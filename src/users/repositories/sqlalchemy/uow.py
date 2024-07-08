from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.users.repositories.sqlalchemy.repo import (
    SQLAlchemyAggregatedUserRepository,
    SQLAlchemyUserRepository,
)
from src.users.repositories.base import AbstractUserUnitOfWork


class SQLAlchemyUserUnitOfWork(BaseSQLAlchemyUnitOfWork, AbstractUserUnitOfWork):
    def __init__(
        self,
        repo: type[SQLAlchemyUserRepository] = SQLAlchemyAggregatedUserRepository,
    ) -> None:
        super().__init__()
        self.repo = repo

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = self.repo(self.session)
