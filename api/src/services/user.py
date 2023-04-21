import uuid

import grpc

from api.generated.model_catalog_pb2 import GrantAccessRequest, SignUpRequest, SignInRequest
from api.src.services.auth_utils import make_password, generate_token, \
    get_user_id_from_context
from api.src.types.exception import ModelCatalogException
from api.src.types.user import User
from database.store import Store


class UserService:
    """
    User service class
    """

    def __init__(self, store: Store) -> None:
        """
        Initializes with the database store
        """
        self.store = store

    def sign_up(self, request: SignUpRequest) -> str:
        """
        Creates a new user
        Args:
            :param request: SignUpRequest
        Returns:
            generated user token
        """
        user_id = str(uuid.uuid4())
        hashed_password = make_password(request.password, user_id)
        user = User(username=request.username, password=hashed_password, user_id=user_id)
        self.store.set_user(user)
        return generate_token(user)

    def sign_in(self, request: SignInRequest) -> str:
        """
        Logs user in
        Args:
            :param request: SignInRequest
        Returns:
            generated user token
        """
        user = self.store.get_user_by_name(request.username)
        hashed_password = make_password(request.password, user.id)
        if user.password != hashed_password:
            raise ModelCatalogException(code=grpc.StatusCode.INVALID_ARGUMENT,
                                        details='Wrong password!')
        return generate_token(user)

    def grant_access(self, request: GrantAccessRequest, context) -> None:
        """
        Grants user access to a folder
        Args:
            :param request: GrantAccessRequest
            :param context
        """
        current_user_id = get_user_id_from_context(context)
        if request.folder_id not in self.store.get_user_folder_permissions(current_user_id):
            raise ModelCatalogException(
                code=grpc.StatusCode.PERMISSION_DENIED,
                details=f"You don't have permission for folder with ID: {request.folder_id}"
            )
        self.store.grant_folder_permission(request.folder_id, request.username)
