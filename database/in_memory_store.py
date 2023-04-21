from collections import defaultdict
from typing import Union

import grpc

from api.src.types.exception import ModelCatalogException
from api.src.types.folder import Folder
from api.src.types.model import Model
from api.src.types.user import User
from api.src.types.version import Version
from database.store import Store


class InMemoryStore(Store):
    """
    In memory implementation store
    """

    def __init__(self):
        self.models = defaultdict(Model)
        self.folders = defaultdict(Folder)
        self.users = defaultdict(User)
        self.folder_permissions = defaultdict(set)
        self.folder_to_models = defaultdict(set)
        self.model_to_folder = defaultdict(str)
        self.user_folder_permissions = defaultdict(set)
        self.user_model_permissions = defaultdict(set)

    def set_model(self, model: Model, user_id: str) -> None:
        self.models[model.id] = model
        self.folder_to_models[model.folder_id].add(model.id)
        self.model_to_folder[model.id] = model.folder_id
        self.user_model_permissions[user_id].add(model.id)

    def get_model(self, model_id: str) -> Model:
        if model_id not in self.models.keys():
            raise ModelCatalogException(code=grpc.StatusCode.INVALID_ARGUMENT,
                                        details=f'Model {model_id} does not exist')
        return self.models[model_id]

    def get_folder_to_model(self, model_id: str) -> str:
        model = self.get_model(model_id)
        return self.model_to_folder[model.id]

    def get_models_to_folder(self, folder_id: str) -> set[str]:
        folder = self.get_folder(folder_id)
        return self.folder_to_models[folder.id]

    def set_folder(self, folder: Folder, user_id: str) -> None:
        user = self.get_user(user_id)
        self.folders[folder.id] = folder
        self.folder_permissions[folder.id].add(user.id)
        self.user_folder_permissions[user.id].add(folder.id)

    def get_folder(self, folder_id: str) -> Folder:
        if folder_id not in self.folders.keys():
            raise ModelCatalogException(code=grpc.StatusCode.INVALID_ARGUMENT,
                                        details=f'Folder {folder_id} does not exist')
        return self.folders[folder_id]

    def set_user(self, user: User) -> None:
        """
        Note: we assume that usernames are unique
        """
        if any(user.username == stored_user.username for stored_user in self.users.values()):
            raise ModelCatalogException(code=grpc.StatusCode.INVALID_ARGUMENT,
                                        details=f'User with name {user.username} already exists')
        self.users[user.id] = user

    def get_user(self, user_id: str) -> User:
        if user_id in self.users.keys():
            return self.users[user_id]

        raise ModelCatalogException(code=grpc.StatusCode.INVALID_ARGUMENT,
                                    details=f'User with id {user_id} does not exist')

    def get_folder_permission(self, folder_id: str) -> set[str]:
        folder = self.get_folder(folder_id)
        return self.folder_permissions[folder.id]

    def grant_folder_permission(self, folder_id: str, username: str) -> None:
        folder = self.get_folder(folder_id)
        user = self.get_user_by_name(username)
        self.folder_permissions[folder.id].add(user.id)
        self.user_folder_permissions[user.id].add(folder.id)
        for model_id in self.folder_to_models[folder.id]:
            self.user_model_permissions[user.id].add(model_id)

    def set_version(self, user_id: str, model_id: str, version: Version) -> None:
        model = self.check_model_user_id(model_id, user_id)
        model.versions.append(version)
        self.set_model(model, user_id)

    def get_version(self, user_id: str, model_id: str, version_id: str) -> Union[Version, None]:
        model = self.check_model_user_id(model_id, user_id)
        for version in self.models[model.id].versions:
            if version.id == version_id:
                return version
        raise ModelCatalogException(code=grpc.StatusCode.INVALID_ARGUMENT,
                                    details=f'Version with ID: {version_id} does not exists')

    def get_user_folder_permissions(self, user_id: str) -> set[str]:
        user = self.get_user(user_id)
        return self.user_folder_permissions[user.id]

    def get_user_models(self, user_id: str) -> list[Model]:
        user = self.get_user(user_id)
        models = []
        for model_id in self.user_model_permissions[user.id]:
            models.append(self.get_model(model_id))
        return models

    def get_user_by_name(self, username: str) -> User:
        """
        Note: In a real database, username would be indexed for quicker retrieval
        """
        for user_id in self.users:
            if self.users[user_id].username == username:
                return self.users[user_id]

        raise ModelCatalogException(code=grpc.StatusCode.INVALID_ARGUMENT,
                                    details=f'User with name {username} does not exist')

    def check_model_user_id(self, model_id, user_id):
        model = self.get_model(model_id)
        if model.id not in self.user_model_permissions[user_id]:
            raise ModelCatalogException(code=grpc.StatusCode.PERMISSION_DENIED,
                                        details=f"You don't have access to model with ID {model_id}")
        return model
