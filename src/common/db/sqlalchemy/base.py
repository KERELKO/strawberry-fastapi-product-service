from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.common.repo import AbstractRepository
from src.common.uow import AbstractUnitOfWork

from .config import async_session_factory


class BaseSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class BaseSQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker = async_session_factory) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()
