import logging
import os

import grpc

from api.generated import model_catalog_pb2_grpc
from api.src.client_services import upload_and_set_version, download_version, sign_up, create_folder, create_model, \
    list_models
from api.src.config import get_config

"""
This file tests uploading of a file, setting an uploaded file as a model version and downloading a specific version
The original file is: new_version.txt, feel free to modify the text.

Do not forget to activate the virtual env and to run the server in another terminal before running this test :

source model_catalog_venv/bin/activate 
python -m api.src.server
"""


def upload_and_download_version(stub):
    # Sign up
    auth = sign_up(stub, 'username-upload', 'fake-password')

    # Create folder
    response_create_folder = create_folder(auth, stub, 'fake-folder-name')

    # Create model
    response_create_model = create_model(auth, stub, response_create_folder.folder_id, 'fake-model', 'fake-description')

    # Create second model
    create_model(auth, stub, response_create_folder.folder_id, 'fake-model-2', 'fake-description-2')

    # Upload and set version to model
    file_to_upload = os.path.join(os.path.dirname(__file__), 'new_version.txt')
    extension = os.path.splitext(os.path.basename(file_to_upload))[1]
    response_upload_version = upload_and_set_version(stub, auth, file_to_upload,
                                                     response_create_model.model_id)

    # List models
    list_models(auth, stub)

    # Download version
    downloaded_file_name = ''.join(['downloaded_version_', response_upload_version.version_id, extension])
    output_download_path = os.path.join(os.path.dirname(__file__), downloaded_file_name)
    download_version(stub, auth, response_create_model.model_id, response_upload_version.version_id,
                     output_download_path)


def run():
    config = get_config()
    channel = grpc.secure_channel(config.address, grpc.ssl_channel_credentials(config.server_crt), )
    stub = model_catalog_pb2_grpc.ModelCatalogStub(channel)
    upload_and_download_version(stub)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
