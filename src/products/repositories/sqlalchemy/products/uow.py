from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.products.repositories.base import AbstractProductUnitOfWork
from src.products.repositories.sqlalchemy.products.repo import SQLAlchemyProductRepository


class SQLAlchemyProductUnitOfWork(AbstractProductUnitOfWork, BaseSQLAlchemyUnitOfWork):
    products: SQLAlchemyProductRepository

    async def __aenter__(self):
        await self.super().__aenter__()
        self.products = SQLAlchemyProductRepository(self.session)
