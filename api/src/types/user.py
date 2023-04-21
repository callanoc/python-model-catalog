class User:
    """
    User type definition
    """

    def __init__(self, username: str, password: str, user_id: str):
        self.id = user_id
        self.username = username
        self.password = password
