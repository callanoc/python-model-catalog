import grpc

from api.generated.model_catalog_pb2 import CreateModelRequest, Model as Model_message, Version
from api.src.services.user import get_user_id_from_context
from api.src.types.exception import ModelCatalogException
from api.src.types.model import Model
from database.store import Store


class ModelService:
    """
    Model service class
    """

    def __init__(self, store: Store):
        """
        Initializes with the database store
        """
        self.store = store

    def create_model(self, request: CreateModelRequest, context) -> str:
        """
        Creates model and set in database
        Args:
            :param request: CreateModelRequest
            :param context
        Returns:
            model id
        """
        user_id = get_user_id_from_context(context)
        if request.folder_id not in self.store.get_user_folder_permissions(user_id):
            raise ModelCatalogException(code=grpc.StatusCode.PERMISSION_DENIED,
                                        details=f"You don't have access to folder with UUID {request.folder_id}")
        model = Model(request.name, request.folder_id, request.description, user_id)
        self.store.set_model(model, user_id)
        return model.id

    def list_models(self, context) -> list[Model_message]:
        """
        List models according to the user permissions
        Args:
            :param context
        Returns:
            list of available models for the current user
        """
        user_id = get_user_id_from_context(context)
        models = self.store.get_user_models(user_id)
        model_list = []
        for model in models:
            version_list = []
            for version in model.versions:
                version_list.append(Version(id=version.id,
                                            file_path=version.file_path))
            model_list.append(Model_message(id=model.id,
                                            name=model.name,
                                            folder_id=model.folder_id,
                                            description=model.description,
                                            versions=version_list,
                                            created_at=model.created_at,
                                            created_by=model.created_by))
        return model_list
