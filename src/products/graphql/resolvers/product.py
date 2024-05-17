from dataclasses import dataclass

import strawberry

from src.products.graphql import schemas
from src.products.repositories.base import AbstractProductUnitOfWork
from src.products.repositories.sqlalchemy.products.uow import SQLAlchemyProductUnitOfWork


@dataclass
class StrawberryProductResolver:
    unit_of_work: AbstractProductUnitOfWork = SQLAlchemyProductUnitOfWork

    async def get_list(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[schemas.Product]:
        ...

    async def get(self, id: int) -> schemas.Product | None:
        ...
