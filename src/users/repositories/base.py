from abc import abstractmethod

from src.common.base.uow import AbstractUnitOfWork
from src.common.base.repo import AbstractRepository
from src.users.dto import UserDTO


class IUserRepository(AbstractRepository[UserDTO]):
    @abstractmethod
    async def get_by_review_id(self, review_id: int, fields: list[str]) -> UserDTO:
        ...


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    users: IUserRepository
