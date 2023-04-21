class ModelCatalogConfig:
    """
    Model catalog config type definition
    """

    def __init__(self,
                 server_crt: bytes,
                 server_key: bytes,
                 address: str,
                 jwt_private_key: bytes,
                 jwt_public_key: bytes,
                 token_expiration: int,
                 chunk_size: int) -> None:
        self.chunk_size = chunk_size
        self.token_expiration = token_expiration
        self.jwt_public_key = jwt_public_key
        self.jwt_private_key = jwt_private_key
        self.address = address
        self.server_crt = server_crt
        self.server_key = server_key
