import time
import uuid

from api.src.types.version import Version


class Model:
    """
    Model type definition
    """

    def __init__(self, name: str, folder_id: str, description: str, username: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.folder_id: str = folder_id
        self.description: str = description
        self.versions: list[Version] = []
        self.created_at: time = time.time()
        self.created_by: str = username
