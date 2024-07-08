from src.common.db.sqlalchemy.base import BaseSQLAlchemyUnitOfWork
from src.products.repositories.base import AbstractReviewUnitOfWork
from src.products.repositories.sqlalchemy.reviews.repo import (
    SQLAlchemyAggregatedReviewRepository, SQLAlchemyReviewRepository
)


class SQLAlchemyReviewUnitOfWork(BaseSQLAlchemyUnitOfWork, AbstractReviewUnitOfWork):
    def __init__(
        self,
        repo: type[SQLAlchemyReviewRepository] = SQLAlchemyAggregatedReviewRepository,
    ) -> None:
        super().__init__()
        self.repo = repo

    async def __aenter__(self):
        await super().__aenter__()
        self.reviews = self.repo(self.session)
