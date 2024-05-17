from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.products.repositories.base import AbstractReviewUnitOfWork
from src.products.repositories.sqlalchemy.reviews.repo import SQLAlchemyReviewRepository


class SQLAlchemyReviewUnitOfWork(BaseSQLAlchemyUnitOfWork, AbstractReviewUnitOfWork):
    reviews: SQLAlchemyReviewRepository

    async def __aenter__(self):
        await super().__aenter__()
        self.reviews = SQLAlchemyReviewRepository(self.session)
