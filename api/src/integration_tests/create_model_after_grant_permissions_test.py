import logging

import grpc

from api.generated import model_catalog_pb2_grpc
from api.src.client_services import sign_up, create_folder, create_model, sign_in, grant_access
from api.src.config import get_config

"""
This file tests if an user can create a model into a folder after being granted access
Do not forget to activate the virtual env and to run the server in another terminal before running this test :

source model_catalog_venv/bin/activate 
python -m api.src.server

"""


def create_model_after_grant_permission(stub):
    username_1 = 'username-grant-1'
    password_1 = 'fake-password-1'
    username_2 = 'username-grant-2'
    password_2 = 'fake-password-2'

    # Sign up first user
    auth = sign_up(stub, username_1, password_1)

    # Create folder
    response_create_folder = create_folder(auth, stub, 'fake-folder-name')

    # Sign up second user
    sign_up(stub, username_2, password_2)

    # Sign in first user
    auth = sign_in(stub, username_1, password_1)

    # Grant access second user to folder
    grant_access(auth, stub, username_2, response_create_folder.folder_id)

    # Sign in as second user
    auth = sign_in(stub, username_2, password_2)

    # Try to create model in folder
    create_model(auth, stub, response_create_folder.folder_id, 'fake-model', 'fake-description')

    logging.info(f'Success!')


def run():
    config = get_config()
    channel = grpc.secure_channel(config.address, grpc.ssl_channel_credentials(config.server_crt), )
    stub = model_catalog_pb2_grpc.ModelCatalogStub(channel)
    create_model_after_grant_permission(stub)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
