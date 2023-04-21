import logging
from concurrent import futures

import grpc

from api.generated import model_catalog_pb2_grpc as model_catalog_grpc
from api.src.config import get_config
from api.src.model_catalog_servicer import ModelCatalogServicer


def run_server():
    """
    Creates a run the server with secure SSL authentication
    """
    config = get_config()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), )
    model_catalog_grpc.add_ModelCatalogServicer_to_server(ModelCatalogServicer(), server)
    server_credentials = grpc.ssl_server_credentials([(config.server_key, config.server_crt)])
    server.add_secure_port(config.address, server_credentials)
    server.start()
    logging.info(f"Server started, listening on {config.address}")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_server()
