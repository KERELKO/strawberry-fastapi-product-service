from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.products.repositories.base import AbstractReviewUnitOfWork
from src.products.repositories.sqlalchemy.reviews.repo import SQLAlchemyReviewRepository


class SQLAlchemyReviewUnitOfWork(AbstractReviewUnitOfWork, BaseSQLAlchemyUnitOfWork):
    products: SQLAlchemyReviewRepository

    async def __aenter__(self):
        await self.super().__aenter__()
        self.products = SQLAlchemyReviewRepository(self.session)
