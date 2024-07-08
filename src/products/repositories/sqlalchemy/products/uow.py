from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.products.repositories.base import AbstractProductUnitOfWork
from src.products.repositories.sqlalchemy.products.repo import (
    SQLAlchemyProductRepository,
    SQLAlchemyAggregatedProductRepository,
)


class SQLAlchemyProductUnitOfWork(BaseSQLAlchemyUnitOfWork, AbstractProductUnitOfWork):
    def __init__(
        self,
        repo: SQLAlchemyProductRepository | SQLAlchemyAggregatedProductRepository,
    ) -> None:
        super().__init__()
        self.repo = repo

    async def __aenter__(self):
        await super().__aenter__()
        self.products = self.repo(self.session)
