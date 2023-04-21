import binascii
import datetime
import hashlib

import grpc
import jwt

from api.src.config import get_config
from api.src.types.exception import ModelCatalogException
from api.src.types.user import User


def make_password(password: str, user_id: str, iterations=100000, hash_name='sha256') -> str:
    """
    Creates a hashed password
    Args:
        :param hash_name
        :param user_id
        :param password
        :param iterations
    Returns:
        hashed password
    """
    dk = hashlib.pbkdf2_hmac(password=password.encode('utf-8'),
                             salt=user_id.encode('utf-8'),
                             iterations=iterations,
                             hash_name=hash_name)
    return binascii.hexlify(dk).decode('ascii')


def generate_token(user: User) -> str:
    """
    Generates user token
    Args:
        :param user
    Returns:
        generated user token
    """
    config = get_config()
    return jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=config.token_expiration)
    }, config.jwt_private_key, algorithm='RS256')


def get_user_id_from_context(context) -> str:
    """
    Retrieves the current user id from the context
    Args:
       :param context
    Returns:
        user idx
    """
    config = get_config()
    metadata = dict(context.invocation_metadata())
    user_token = metadata['user_token']

    user_id = jwt.decode(user_token, key=config.jwt_public_key, algorithms=['RS256']).get('user_id')
    if user_id is None:
        raise ModelCatalogException(code=grpc.StatusCode.UNAUTHENTICATED,
                                    details='Invalid token')
    return user_id
