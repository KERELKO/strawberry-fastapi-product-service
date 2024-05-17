from sqlalchemy.ext.asyncio import async_sessionmaker

from src.common.db.sqlalchemy import async_session_factory
from src.common.uow import AbstractUnitOfWork
from src.users.repositories.sqlalchemy.repo import SQLAlchemyUserRepository
from src.users.repositories.base import AbstractUserRepository


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    users: AbstractUserRepository


class SQLAlchemyUserUnitOfWork(AbstractUserUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker = async_session_factory) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = SQLAlchemyUserRepository(self.session)

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)

    async def rollback(self) -> None:
        await self.session.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()
