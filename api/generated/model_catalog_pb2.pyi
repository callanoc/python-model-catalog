from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateFolderRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateFolderResponse(_message.Message):
    __slots__ = ["folder_id"]
    FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
    folder_id: str
    def __init__(self, folder_id: _Optional[str] = ...) -> None: ...

class CreateModelRequest(_message.Message):
    __slots__ = ["description", "folder_id", "name"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    description: str
    folder_id: str
    name: str
    def __init__(self, name: _Optional[str] = ..., folder_id: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateModelResponse(_message.Message):
    __slots__ = ["model_id"]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    def __init__(self, model_id: _Optional[str] = ...) -> None: ...

class DownloadVersionRequest(_message.Message):
    __slots__ = ["model_id", "version_id"]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    version_id: str
    def __init__(self, model_id: _Optional[str] = ..., version_id: _Optional[str] = ...) -> None: ...

class DownloadVersionResponse(_message.Message):
    __slots__ = ["chunk_data"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    def __init__(self, chunk_data: _Optional[bytes] = ...) -> None: ...

class FileMetadata(_message.Message):
    __slots__ = ["filename", "model_id"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    filename: str
    model_id: str
    def __init__(self, filename: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class GrantAccessRequest(_message.Message):
    __slots__ = ["folder_id", "username"]
    FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    folder_id: str
    username: str
    def __init__(self, username: _Optional[str] = ..., folder_id: _Optional[str] = ...) -> None: ...

class GrantAccessResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class ListModelsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListModelsResponse(_message.Message):
    __slots__ = ["model"]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: _containers.RepeatedCompositeFieldContainer[Model]
    def __init__(self, model: _Optional[_Iterable[_Union[Model, _Mapping]]] = ...) -> None: ...

class Model(_message.Message):
    __slots__ = ["created_at", "created_by", "description", "folder_id", "id", "name", "versions"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    created_at: float
    created_by: str
    description: str
    folder_id: str
    id: str
    name: str
    versions: _containers.RepeatedCompositeFieldContainer[Version]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., folder_id: _Optional[str] = ..., description: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[Version, _Mapping]]] = ..., created_at: _Optional[float] = ..., created_by: _Optional[str] = ...) -> None: ...

class SetModelVersionRequest(_message.Message):
    __slots__ = ["model_id", "uploaded_file_path"]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    UPLOADED_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    uploaded_file_path: str
    def __init__(self, model_id: _Optional[str] = ..., uploaded_file_path: _Optional[str] = ...) -> None: ...

class SetModelVersionResponse(_message.Message):
    __slots__ = ["version_id"]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    version_id: str
    def __init__(self, version_id: _Optional[str] = ...) -> None: ...

class SignInRequest(_message.Message):
    __slots__ = ["password", "username"]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    password: str
    username: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class SignInResponse(_message.Message):
    __slots__ = ["token"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class SignUpRequest(_message.Message):
    __slots__ = ["password", "username"]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    password: str
    username: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class SignUpResponse(_message.Message):
    __slots__ = ["token"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class UploadFileRequest(_message.Message):
    __slots__ = ["chunk_data", "file_metadata"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    FILE_METADATA_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    file_metadata: FileMetadata
    def __init__(self, file_metadata: _Optional[_Union[FileMetadata, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ["file_path"]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    def __init__(self, file_path: _Optional[str] = ...) -> None: ...

class Version(_message.Message):
    __slots__ = ["file_path", "id"]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    id: str
    def __init__(self, id: _Optional[str] = ..., file_path: _Optional[str] = ...) -> None: ...
