from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.users.repositories.sqlalchemy.repo import SQLAlchemyUserRepository
from src.users.repositories.base import AbstractUserUnitOfWork


class SQLAlchemyUserUnitOfWork(BaseSQLAlchemyUnitOfWork, AbstractUserUnitOfWork):
    def __init__(self, repo: SQLAlchemyUserRepository) -> None:
        self.repo = repo

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = self.repo(self.session)
