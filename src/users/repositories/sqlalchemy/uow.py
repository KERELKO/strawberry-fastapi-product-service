from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.users.repositories.sqlalchemy.repo import SQLAlchemyUserRepository
from src.users.repositories.base import AbstractUserUnitOfWork


class SQLAlchemyUserUnitOfWork(AbstractUserUnitOfWork, BaseSQLAlchemyUnitOfWork):
    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = SQLAlchemyUserRepository(self.session)
