import logging

import grpc

from api.generated import model_catalog_pb2_grpc
from api.src.client_services import sign_up, create_folder, create_model, grant_access, list_models, sign_in
from api.src.config import get_config

"""
This file allows users to interact with the server with several actions:
    - Create folder
    - Create model
    - List models
    - Grant access to folder
    - Sign up
    - Sign in
Do not forget to activate the virtual env and to run the server in another terminal before running this test :

source model_catalog_venv/bin/activate 
python -m api.src.server
"""


def run():
    config = get_config()
    channel = grpc.secure_channel(config.address, grpc.ssl_channel_credentials(config.server_crt), )
    stub = model_catalog_pb2_grpc.ModelCatalogStub(channel)
    logging.info("Welcome to the Model Catalog API!")
    rpc_username = input(f"Please enter the username: ")
    rpc_password = input(f"\nPlease enter the password: ")
    auth = sign_up(stub, rpc_username, rpc_password)
    action_display = "\n1. Create folder\n2. Create model\n3. List models\n4. Grant access to folder\n5. Sign up\n6. Sign in\n7. Quit"
    logging.info(action_display)
    rpc_call = ""
    while rpc_call != "7":
        rpc_call = input("Which action would you like to do? ")
        match rpc_call:
            case "1":
                rpc_folder_name = input("\nPlease enter folder name: ")
                create_folder(auth, stub, rpc_folder_name)
            case "2":
                rpc_model_folder_id = input("\nPlease enter folder ID: ")
                rpc_model_name = input("\nPlease enter model name: ")
                rpc_model_description = input("\nPlease enter model description: ")
                create_model(auth, stub, rpc_model_folder_id, rpc_model_name, rpc_model_description)
            case "3":
                logging.info(list_models(auth, stub))
            case "4":
                rpc_username = input("\nPlease enter the username: ")
                rpc_folder_id = input("\nPlease enter folder ID: ")
                grant_access(auth, stub, rpc_username, rpc_folder_id)
            case "5":
                rpc_username = input(f"Please enter the username: ")
                rpc_password = input(f"\nPlease enter the password: ")
                auth = sign_up(stub, rpc_username, rpc_password)
            case "6":
                rpc_username = input(f"Please enter your username: ")
                rpc_password = input(f"\nPlease enter your password: ")
                auth = sign_in(stub, rpc_username, rpc_password)
            case "7":
                logging.info("Thank you for using the Model Catalog API, Goodbye!")
            case _:
                logging.info(action_display)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
