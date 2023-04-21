import logging

from api.generated import model_catalog_pb2
from api.generated.model_catalog_pb2 import SetModelVersionResponse, CreateFolderResponse, CreateModelResponse, \
    GrantAccessResponse, ListModelsResponse
from api.src.config import get_config

"""
Services for client side
"""


def sign_up(stub, username: str, password: str):
    """
    Sign up client method
    """
    sign_up_request = model_catalog_pb2.SignUpRequest(username=username, password=password)
    response_sign_up = stub.SignUp(sign_up_request)
    logging.info(f'Sign up: {response_sign_up}')
    auth = [('user_token', response_sign_up.token)]
    return auth


def sign_in(stub, username: str, password: str):
    """
    Sign in client method
    """
    sign_in_request = model_catalog_pb2.SignInRequest(username=username, password=password)
    response_sign_in = stub.SignIn(sign_in_request)
    logging.info(f'Sign in: {response_sign_in}')
    auth = [('user_token', response_sign_in.token)]
    return auth


def create_folder(auth, stub, folder_name: str) -> CreateFolderResponse:
    """
    Create folder client method
    """
    create_folder_request = model_catalog_pb2.CreateFolderRequest(name=folder_name)
    response_create_folder = stub.CreateFolder(create_folder_request, metadata=auth)
    logging.info(f'Create folder: {response_create_folder}')
    return response_create_folder


def create_model(auth, stub, folder_id: str, model_name: str, description: str) -> CreateModelResponse:
    """
    Create model client method
    """
    create_model_request = model_catalog_pb2.CreateModelRequest(name=model_name,
                                                                folder_id=folder_id,
                                                                description=description)
    response_create_model = stub.CreateModel(create_model_request, metadata=auth)
    logging.info(f'Create model: {response_create_model}')
    return response_create_model


def grant_access(auth, stub, username: str, folder_id: str) -> GrantAccessResponse:
    """
    Grant user access client method
    """
    grant_access_request = model_catalog_pb2.GrantAccessRequest(username=username, folder_id=folder_id)
    response_grand_access = stub.GrantAccess(grant_access_request, metadata=auth)
    logging.info(f'Grant access: {response_grand_access}')
    return response_grand_access


def upload_and_set_version(stub, auth, file_to_upload: str, model_id: str) -> SetModelVersionResponse:
    """
    Upload and set model version client method
    """
    response_upload_file = stub.UploadFile(upload(file_to_upload, model_id))
    logging.info(f'Upload file: {response_upload_file}')
    set_version_request = model_catalog_pb2.SetModelVersionRequest(model_id=model_id,
                                                                   uploaded_file_path=response_upload_file.file_path)
    response_set_version = stub.SetModelVersion(set_version_request, metadata=auth)
    logging.info(f'Set model version: {response_set_version}')
    return response_set_version


def upload(input_path: str, model_id: str):
    """
    Upload method for upload file stream request
    """
    config = get_config()
    file_metadata = model_catalog_pb2.FileMetadata(model_id=model_id, filename=input_path)
    yield model_catalog_pb2.UploadFileRequest(file_metadata=file_metadata)
    with open(input_path, mode='rb') as file_to_upload:
        while True:
            chunk = file_to_upload.read(config.chunk_size)
            if chunk:
                upload_request = model_catalog_pb2.UploadFileRequest(chunk_data=chunk)
                yield upload_request
            else:
                return


def download_version(stub, auth, model_id: str, version_id: str, output_path: str) -> None:
    """
    Download version client method
    """
    download_version_request = model_catalog_pb2.DownloadVersionRequest(model_id=model_id, version_id=version_id)
    for download_response in stub.DownloadVersion(download_version_request, metadata=auth):
        with open(output_path, mode="wb") as f:
            f.write(download_response.chunk_data)
    logging.info(f'Successfully downloaded here :{output_path}')


def list_models(auth, stub) -> ListModelsResponse:
    """
    List models client method
    """
    response_list_models = stub.ListModels(model_catalog_pb2.ListModelsRequest(), metadata=auth)
    logging.info(f'List models: {response_list_models}')
    return response_list_models
