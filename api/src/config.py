import os
from pathlib import Path
from typing import Union

import yaml

from api.src.types.config import ModelCatalogConfig

loaded_config: Union[ModelCatalogConfig, None] = None


def get_config() -> ModelCatalogConfig:
    """
    Sets config constants once and returns it
    Returns:
        config: ModelCatalogConfig
    """
    global loaded_config
    if loaded_config is not None:
        return loaded_config

    constants = yaml.safe_load(load_file('constants.yml'))
    loaded_config = ModelCatalogConfig(
        server_crt=load_file(constants['SERVER_CRT_PATH']),
        server_key=load_file(constants['SERVER_KEY_PATH']),
        jwt_public_key=load_file(constants['JWT_PUBLIC_KEY_PATH']),
        jwt_private_key=load_file(constants['JWT_PRIVATE_KEY_PATH']),
        address=constants['ADDRESS'],
        chunk_size=constants['CHUNK_SIZE'],
        token_expiration=constants['TOKEN_EXPIRATION'],
    )

    return loaded_config


def load_file(path: str) -> bytes:
    """
    Loads file contents
    Args:
        :param path
    Returns:
        file contents
    """
    with open(Path(os.path.join(os.path.dirname(__file__), path)), 'rb') as file_content:
        return file_content.read()
