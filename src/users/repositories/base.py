from src.common.base.uow import AbstractUnitOfWork
from src.common.base.repo import AbstractRepository
from src.users.dto import UserDTO


class AbstractUserRepository(AbstractRepository[UserDTO]):
    ...


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    users: AbstractUserRepository
