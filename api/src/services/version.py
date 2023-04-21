import os
from pathlib import Path

import grpc

from api.generated.model_catalog_pb2 import UploadFileResponse, \
    DownloadVersionResponse, DownloadVersionRequest, SetModelVersionRequest
from api.src.config import get_config
from api.src.services.auth_utils import get_user_id_from_context
from api.src.types.exception import ModelCatalogException
from api.src.types.version import Version
from database.store import Store


class VersionService:
    """
    Version service class
    """

    def __init__(self, store: Store):
        """
        Initializes with the database store
        """
        self.store = store

    @staticmethod
    def check_upload_path(filename: str) -> None:
        """
        Directory traversal check
        Args:
            :param filename
        """
        root_dir = Path(os.path.dirname(__file__))
        try:
            Path(root_dir).joinpath(filename).resolve().relative_to(root_dir.resolve())
        except ValueError:
            raise ModelCatalogException(code=grpc.StatusCode.INVALID_ARGUMENT,
                                        details='The input filename is incorrect, please avoid directory traversal')

    def generate_upload_file_path(self, model_id: str, filename: str) -> str:
        """
        Generates the output file path and checks if it stays in the current directory to avoid directory traversal attacks
        Args:
            :param model_id
            :param filename
        Returns:
            upload file path
        """
        folder_name = ''.join(['uploaded_versions_', model_id])
        root_dir = Path(os.path.dirname(__file__))
        folder_path = Path(os.path.join(root_dir, folder_name))
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        output_file_path = str(Path(os.path.join(folder_path, os.path.basename(filename))))
        self.check_upload_path(output_file_path)
        if os.path.exists(output_file_path):
            output_file_path = ''.join(['new_', output_file_path])
        return output_file_path

    def upload_file(self, request_iterator) -> UploadFileResponse:
        """
        Uploads file
        Args:
            :param request_iterator: request iterator (stream request)
        Returns:
            UploadFileResponse with the uploaded file path
        """
        data = bytearray()
        uploaded_file_path = ''
        for request in request_iterator:
            if uploaded_file_path == '' and request.file_metadata.filename:
                uploaded_file_path = self.generate_upload_file_path(request.file_metadata.model_id,
                                                                    request.file_metadata.filename)
                continue
            data.extend(request.chunk_data)
        with open(uploaded_file_path, mode='wb+') as uploaded_file:
            uploaded_file.write(data)
        return UploadFileResponse(file_path=uploaded_file_path)

    def set_model_version(self, request: SetModelVersionRequest, context) -> str:
        """
        Set uploaded version file to model
        Args:
            :param context
            :param request: SetModelVersionRequest
        Returns:
            version id
        """
        user_id = get_user_id_from_context(context)
        version = Version(file_path=request.uploaded_file_path)
        self.store.set_version(user_id, request.model_id, version)
        return version.id

    def download_version(self, request: DownloadVersionRequest, context) -> DownloadVersionResponse:
        """
        Downloads version
        Args:
            :param request: DownloadVersionRequest
            :param context
        Returns:
            DownloadVersionResponse (stream response)
        """
        user_id = get_user_id_from_context(context)
        version = self.store.get_version(user_id, request.model_id, request.version_id)
        config = get_config()
        with open(version.file_path, mode="rb") as downloaded_file:
            while True:
                chunk = downloaded_file.read(config.chunk_size)
                if chunk:
                    entry_response = DownloadVersionResponse(chunk_data=chunk)
                    yield entry_response
                else:  # EOF
                    return
