from dataclasses import dataclass

import strawberry

from src.products.graphql import schemas
from src.products.repositories.base import AbstractReviewUnitOfWork
from src.products.repositories.sqlalchemy.reviews.uow import SQLAlchemyReviewRepository


@dataclass
class StrawberryReviewResolver:
    unit_of_work: AbstractReviewUnitOfWork = SQLAlchemyReviewRepository

    async def get_list(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[schemas.Review]:
        ...

    async def get(self, id: int) -> schemas.Review | None:
        ...
