from src.common.base.uow import AbstractUnitOfWork
from src.users.repositories.mongo.repo import MongoUserRepository


class FakeMongoUnitOfWork(AbstractUnitOfWork):
    users: MongoUserRepository

    async def __aenter__(self) -> None:
        self.users = MongoUserRepository()

    async def __aexit__(self, *args) -> None:
        await self.rollback()

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
