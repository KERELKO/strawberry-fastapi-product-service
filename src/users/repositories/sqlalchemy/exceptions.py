class NoUserIDException(Exception):
    def __str__(self) -> str:
        return 'ID for the user is not provided'
