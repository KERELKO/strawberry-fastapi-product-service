from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.products.repositories.base import AbstractReviewUnitOfWork
from src.products.repositories.sqlalchemy.reviews.repo import (
    SQLAlchemyAggregatedReviewRepository
)


class SQLAlchemyReviewUnitOfWork(BaseSQLAlchemyUnitOfWork, AbstractReviewUnitOfWork):
    reviews: SQLAlchemyAggregatedReviewRepository

    async def __aenter__(self):
        await super().__aenter__()
        self.reviews = SQLAlchemyAggregatedReviewRepository(self.session)
