import logging

import grpc
import pytest

from api.generated import model_catalog_pb2_grpc
from api.src.client_services import sign_up, create_folder, create_model
from api.src.config import get_config

"""
This file tests if an exception is thrown when an user tries to create a model in a folder 
without permission.
Do not forget to activate the virtual env and to run the server in another terminal before running this test :

source model_catalog_venv/bin/activate 
python -m api.src.server
"""


def test_create_model_without_folder_permission(stub):
    # Sign up first user
    auth = sign_up(stub, 'username-folder-permission-1', 'fake-password-1')

    # Create folder
    response_create_folder = create_folder(auth, stub, 'fake-folder-name')

    # Sign up second user
    auth = sign_up(stub, 'username-folder-permission-2', 'fake-password-2')

    # Try to create model in folder without permission
    with pytest.raises(Exception):
        create_model(auth, stub, response_create_folder.folder_id, 'fake-model', 'fake-description')

    logging.info('Exception thrown successfully!')


def run():
    config = get_config()
    channel = grpc.secure_channel(config.address, grpc.ssl_channel_credentials(config.server_crt), )
    stub = model_catalog_pb2_grpc.ModelCatalogStub(channel)
    test_create_model_without_folder_permission(stub)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
