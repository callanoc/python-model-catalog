import uuid


class Folder:
    """
    Folder type definition
    """

    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
