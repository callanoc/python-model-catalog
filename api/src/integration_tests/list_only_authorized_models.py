import logging

import grpc

from api.generated import model_catalog_pb2_grpc
from api.src.client_services import sign_up, create_folder, create_model, sign_in, list_models, grant_access
from api.src.config import get_config

"""
This file tests the list method only lists authorized models according to the user permissions
Do not forget to activate the virtual env and to run the server in another terminal before running this test :

source model_catalog_venv/bin/activate 
python -m api.src.server
"""


def list_only_authorized_models(stub):
    username_1 = 'username-list-1'
    password_1 = 'fake-password-1'
    username_2 = 'username-list-2'
    password_2 = 'fake-password-2'

    # Sign up first user
    auth = sign_up(stub, username_1, password_1)

    # Create folder
    response_create_folder = create_folder(auth, stub, 'fake-folder-name')

    # Create a first model
    create_model(auth, stub, response_create_folder.folder_id, 'fake-model-1', 'fake-description-1')

    # Create a second model
    create_model(auth, stub, response_create_folder.folder_id, 'fake-model-2', 'fake-description-2')

    # Sign up second user
    auth = sign_up(stub, username_2, password_2)

    # Create a new folder
    response_create_folder_2 = create_folder(auth, stub, 'fake-folder-name-2')

    # Create a model
    create_model(auth, stub, response_create_folder_2.folder_id, 'fake-model-3', 'fake-description-3')

    # Sign in first user
    auth = sign_in(stub, username_1, password_1)

    # List models (only 2 models)
    list_models(auth, stub)

    # Sign in second user
    auth = sign_in(stub, username_2, password_2)

    # Grant access to second folder to first user
    grant_access(auth, stub, username_1, response_create_folder_2.folder_id)

    # Sign back in first user
    auth = sign_in(stub, username_1, password_1)

    # List models (3 models)
    list_models(auth, stub)

    logging.info(f'Success!')


def run():
    config = get_config()
    channel = grpc.secure_channel(config.address, grpc.ssl_channel_credentials(config.server_crt), )
    stub = model_catalog_pb2_grpc.ModelCatalogStub(channel)
    list_only_authorized_models(stub)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
