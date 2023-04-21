from api.generated import model_catalog_pb2_grpc as model_catalog_grpc
from api.generated.model_catalog_pb2 import CreateFolderResponse, CreateModelResponse, \
    ListModelsResponse, GrantAccessResponse, CreateFolderRequest, CreateModelRequest, \
    GrantAccessRequest, SignUpRequest, SignUpResponse, SignInRequest, SignInResponse, \
    UploadFileResponse, DownloadVersionRequest, DownloadVersionResponse, \
    SetModelVersionRequest, SetModelVersionResponse
from api.src.services.folder import FolderService
from api.src.services.model import ModelService
from api.src.services.user import UserService
from api.src.services.version import VersionService
from api.src.types.exception import GrpcExceptionHandler
from database.in_memory_store import InMemoryStore


class ModelCatalogServicer(model_catalog_grpc.ModelCatalogServicer):
    """
    Model catalog servicer class
    contains rpc call methods
    """

    def __init__(self):
        """
        Initializes database store and services
        """
        self.store = InMemoryStore()
        self.model_service = ModelService(self.store)
        self.folder_service = FolderService(self.store)
        self.user_service = UserService(self.store)
        self.version_service = VersionService(self.store)

    @GrpcExceptionHandler()
    def SignUp(self, request: SignUpRequest, context) -> SignUpResponse:
        """
        Sign up method
        """
        token = self.user_service.sign_up(request)
        return SignUpResponse(token=token)

    @GrpcExceptionHandler()
    def SignIn(self, request: SignInRequest, context) -> SignInResponse:
        """
        Sign in method
        """
        token = self.user_service.sign_in(request)
        return SignInResponse(token=token)

    @GrpcExceptionHandler()
    def CreateFolder(self, request: CreateFolderRequest, context) -> CreateFolderResponse:
        """
        Create folder method
        """
        folder_id = self.folder_service.create_folder(request, context)
        return CreateFolderResponse(folder_id=folder_id)

    @GrpcExceptionHandler()
    def CreateModel(self, request: CreateModelRequest, context) -> CreateModelResponse:
        """
        Create model method
        """
        model_id = self.model_service.create_model(request, context)
        return CreateModelResponse(model_id=model_id)

    @GrpcExceptionHandler()
    def GrantAccess(self, request: GrantAccessRequest, context) -> GrantAccessResponse:
        """
        Grant access method
        """
        self.user_service.grant_access(request, context)
        return GrantAccessResponse()

    @GrpcExceptionHandler()
    def ListModels(self, _, context) -> ListModelsResponse:
        """
        List models method
        """
        return ListModelsResponse(model=self.model_service.list_models(context))

    @GrpcExceptionHandler()
    def UploadFile(self, request_iterator, context) -> UploadFileResponse:
        """
        Upload file method
        """
        return self.version_service.upload_file(request_iterator)

    @GrpcExceptionHandler()
    def SetModelVersion(self, request: SetModelVersionRequest, context) -> SetModelVersionResponse:
        """
        Set model method
        """
        return SetModelVersionResponse(version_id=self.version_service.set_model_version(request, context))

    @GrpcExceptionHandler()
    def DownloadVersion(self, request: DownloadVersionRequest, context) -> DownloadVersionResponse:
        """
        Download version method
        """
        return self.version_service.download_version(request, context)
