from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.products.repositories.base import AbstractReviewUnitOfWork
from src.products.repositories.sqlalchemy.reviews.repo import (
    SQLAlchemyAggregatedReviewRepository, SQLAlchemyReviewRepository
)


class SQLAlchemyReviewUnitOfWork(BaseSQLAlchemyUnitOfWork, AbstractReviewUnitOfWork):
    def __init__(
        self,
        repo: SQLAlchemyReviewRepository | SQLAlchemyAggregatedReviewRepository,
    ) -> None:
        self.repo = repo

    async def __aenter__(self):
        await super().__aenter__()
        self.reviews = self.repo(self.session)
