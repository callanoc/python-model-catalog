from abc import ABC, abstractmethod
from typing import Union

from api.src.types.folder import Folder
from api.src.types.model import Model
from api.src.types.user import User
from api.src.types.version import Version


class Store(ABC):
    """
    Abstract store class
    """

    @abstractmethod
    def set_model(self, model: Model, user_id: str) -> None:
        pass

    @abstractmethod
    def get_model(self, model_id: str) -> Model:
        pass

    @abstractmethod
    def get_folder_to_model(self, model_id: str) -> str:
        pass

    @abstractmethod
    def get_models_to_folder(self, folder_id: str) -> set[str]:
        pass

    @abstractmethod
    def set_folder(self, folder: Folder, user_id: str) -> None:
        pass

    @abstractmethod
    def get_folder(self, folder_id: str) -> Folder:
        pass

    @abstractmethod
    def set_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def get_folder_permission(self, folder_id: str) -> set[str]:
        pass

    @abstractmethod
    def grant_folder_permission(self, folder_id: str, username: str) -> None:
        pass

    @abstractmethod
    def set_version(self, user_id: str, model_id: str, version: Version) -> None:
        pass

    @abstractmethod
    def get_version(self, user_id: str, model_id: str, version_id: str) -> Union[Version, None]:
        pass

    @abstractmethod
    def get_user_folder_permissions(self, user_id: str) -> set[str]:
        pass

    @abstractmethod
    def get_user_models(self, user_id: str) -> list[Model]:
        pass

    @abstractmethod
    def get_user_by_name(self, username: str) -> User:
        pass
