import uuid


class Version:
    """
    Version type definition
    """

    def __init__(self, file_path: str):
        self.id: str = str(uuid.uuid4())
        self.file_path = file_path
