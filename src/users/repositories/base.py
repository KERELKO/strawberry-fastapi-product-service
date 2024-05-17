from src.common.repo import AbstractRepository
from src.users.dto import UserDTO


class AbstractUserRepository[UserDTO](AbstractRepository):
    ...
