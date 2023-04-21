from api.generated.model_catalog_pb2 import CreateFolderRequest
from api.src.services.user import get_user_id_from_context
from api.src.types.folder import Folder
from database.store import Store


class FolderService:
    """
    Folder service class
    """

    def __init__(self, store: Store):
        """
        Initializes with the database store
        """
        self.store = store

    def create_folder(self, request: CreateFolderRequest, context) -> str:
        """
        Creates a folder
        Args:
            :param request: CreateFolderRequest
            :param context
        Returns:
            folder id
        """
        user_id = get_user_id_from_context(context)
        folder = Folder(request.name)
        self.store.set_folder(folder, user_id)
        return folder.id
