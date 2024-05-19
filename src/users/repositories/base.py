from src.common.uow import AbstractUnitOfWork
from src.common.repo import AbstractRepository
from src.users.dto import UserDTO


class AbstractUserRepository(AbstractRepository[UserDTO]):
    ...


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    users: AbstractUserRepository
