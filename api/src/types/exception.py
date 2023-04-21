import functools

from grpc import StatusCode


class ModelCatalogException(Exception):
    """
    Model catalog custom exception type with code and details to return when aborting context
    """

    def __init__(self, code: StatusCode, details: str):
        self.code = code
        self.details = details
        super().__init__(details)


def GrpcExceptionHandler():
    """
    Exception handler decorator which aborts context when a ModelCatalogException is raised
    """

    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ModelCatalogException as e:
                context = args[2]
                context.abort(e.code, e.details)

        return inner

    return wrapper
