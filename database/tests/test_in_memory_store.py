import grpc

from api.src.types.exception import ModelCatalogException
from api.src.types.folder import Folder
from api.src.types.model import Model
from api.src.types.user import User
from api.src.types.version import Version
from database.in_memory_store import InMemoryStore

MOCK_FOLDER = Folder('fake-folder-name')
MOCK_MODEL = Model('fake-model-name', MOCK_FOLDER.id, 'fake-description', 'fake-user-id')
MOCK_MODEL_2 = Model('fake-model-name-2', MOCK_FOLDER.id, 'fake-description-2', 'fake-user-id-2')
MOCK_USER = User('fake-username', 'fake-password', 'fake-id')
MOCK_USER_SAME_USERNAME = User('fake-username', 'fake-pass', 'fake-id-')
MOCK_USER_2 = User('fake-username-2', 'fake-password-2', 'fake-id-2')
MOCK_VERSION = Version('fake-file-path')


def test_set_model():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    assert MOCK_STORE.get_model(MOCK_MODEL.id) == MOCK_MODEL
    assert MOCK_MODEL.id in MOCK_STORE.get_models_to_folder(MOCK_FOLDER.id)
    assert MOCK_STORE.get_folder_to_model(MOCK_MODEL.id) == MOCK_FOLDER.id
    assert MOCK_STORE.get_user_models(MOCK_USER.id) == [MOCK_MODEL]


def test_get_folder_permission_when_folder_exists():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    assert MOCK_STORE.get_folder(MOCK_FOLDER.id) == MOCK_FOLDER
    assert MOCK_USER.id in MOCK_STORE.get_folder_permission(MOCK_FOLDER.id)


def test_get_folder_permission_when_folder_does_not_exist():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    try:
        MOCK_STORE.get_folder_permission(MOCK_FOLDER.id) == MOCK_USER.id
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'Folder {MOCK_FOLDER.id} does not exist'


def test_grant_folder_permission_correct():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_user(MOCK_USER_2)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    MOCK_STORE.grant_folder_permission(MOCK_FOLDER.id, MOCK_USER_2.username)
    assert MOCK_USER.id in MOCK_STORE.get_folder_permission(MOCK_FOLDER.id)
    assert MOCK_STORE.get_user_folder_permissions(MOCK_USER_2.id) == {MOCK_FOLDER.id}
    assert MOCK_MODEL in MOCK_STORE.get_user_models(MOCK_USER_2.id)


def test_grant_folder_permission_when_folder_does_not_exist():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    try:
        MOCK_STORE.grant_folder_permission(MOCK_FOLDER.id, MOCK_USER.username)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'Folder {MOCK_FOLDER.id} does not exist'


def test_grant_folder_permission_when_user_does_not_exist():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    try:
        MOCK_STORE.grant_folder_permission(MOCK_FOLDER.id, MOCK_USER_2.username)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'User with name {MOCK_USER_2.username} does not exist'


def test_get_user_folder_permissions_correct():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    assert MOCK_STORE.get_user_folder_permissions(MOCK_USER.id) == {MOCK_FOLDER.id}


def test_get_user_folder_permissions_when_folder_does_not_exist():
    MOCK_STORE = InMemoryStore()
    try:
        assert MOCK_STORE.get_user_folder_permissions(MOCK_USER.id) == MOCK_FOLDER.id
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'User with id {MOCK_USER.id} does not exist'


def test_get_user_models_correct():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL_2, MOCK_USER.id)
    assert len(MOCK_STORE.get_user_models(MOCK_USER.id)) == 2


def test_get_user_models_when_user_does_not_exist():
    MOCK_STORE = InMemoryStore()
    try:
        MOCK_STORE.get_user_folder_permissions(MOCK_USER.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'User with id {MOCK_USER.id} does not exist'


def test_get_model_when_id_does_not_exists():
    MOCK_STORE = InMemoryStore()
    try:
        MOCK_STORE.get_model(MOCK_MODEL.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'Model {MOCK_MODEL.id} does not exist'


def test_get_folder_to_model_correct():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    assert MOCK_STORE.get_folder_to_model(MOCK_MODEL.id) == MOCK_FOLDER.id


def test_get_folder_to_model_when_model_does_not_exist():
    MOCK_STORE = InMemoryStore()
    try:
        MOCK_STORE.get_folder_to_model(MOCK_MODEL.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'Model {MOCK_MODEL.id} does not exist'


def test_get_models_to_folder_correct():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL_2, MOCK_USER.id)
    assert MOCK_STORE.get_models_to_folder(MOCK_FOLDER.id) == {MOCK_MODEL.id, MOCK_MODEL_2.id}


def test_get_models_to_folder_when_folder_does_not_exist():
    MOCK_STORE = InMemoryStore()
    try:
        MOCK_STORE.get_models_to_folder(MOCK_FOLDER.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'Folder {MOCK_FOLDER.id} does not exist'


def test_set_folder_correct():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    assert MOCK_STORE.get_user_folder_permissions(MOCK_USER.id) == {MOCK_FOLDER.id}


def test_set_folder_when_user_does_not_exist():
    MOCK_STORE = InMemoryStore()
    try:
        MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'User with id {MOCK_USER.id} does not exist'


def test_get_folder_when_id_does_not_exist():
    MOCK_STORE = InMemoryStore()
    try:
        MOCK_STORE.get_folder(MOCK_FOLDER.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'Folder {MOCK_FOLDER.id} does not exist'


def test_set_user_when_username_is_already_taken():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    try:
        MOCK_STORE.set_user(MOCK_USER_SAME_USERNAME)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'User with name {MOCK_USER_SAME_USERNAME.username} already exists'


def test_get_user():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    assert MOCK_STORE.get_user(MOCK_USER.id) == MOCK_USER


def test_get_user_by_name():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    assert MOCK_STORE.get_user_by_name(MOCK_USER.username) == MOCK_USER


def test_check_model_user_id_correct():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    assert MOCK_STORE.check_model_user_id(MOCK_MODEL.id, MOCK_USER.id) == MOCK_MODEL


def test_check_model_user_id_when_model_does_not_exist():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    try:
        MOCK_STORE.check_model_user_id(MOCK_MODEL.id, MOCK_USER.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'Model {MOCK_MODEL.id} does not exist'


def test_check_model_user_id_when_user_is_not_authorized():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_user(MOCK_USER_2)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    try:
        MOCK_STORE.check_model_user_id(MOCK_MODEL.id, MOCK_USER_2.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.PERMISSION_DENIED
        assert e.details == f"You don't have access to model with ID {MOCK_MODEL.id}"


def test_get_version_correct():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    MOCK_STORE.set_version(MOCK_USER.id, MOCK_MODEL.id, MOCK_VERSION)
    assert MOCK_STORE.get_version(MOCK_USER.id, MOCK_MODEL.id, MOCK_VERSION.id) == MOCK_VERSION


def test_get_version_when_version_does_not_exist():
    MOCK_STORE = InMemoryStore()
    MOCK_STORE.set_user(MOCK_USER)
    MOCK_STORE.set_folder(MOCK_FOLDER, MOCK_USER.id)
    MOCK_STORE.set_model(MOCK_MODEL, MOCK_USER.id)
    try:
        MOCK_STORE.get_version(MOCK_USER.id, MOCK_MODEL.id, MOCK_VERSION.id)
    except ModelCatalogException as e:
        assert e.code == grpc.StatusCode.INVALID_ARGUMENT
        assert e.details == f'Version with ID: {MOCK_VERSION.id} does not exists'
