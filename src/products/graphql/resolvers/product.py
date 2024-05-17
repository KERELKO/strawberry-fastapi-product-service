from dataclasses import dataclass
from typing import Type

import strawberry
from strawberry.utils.str_converters import to_snake_case

from src.products.graphql import schemas
from src.products.repositories.base import AbstractProductUnitOfWork
from src.products.repositories.sqlalchemy.products.uow import SQLAlchemyProductUnitOfWork


@dataclass
class StrawberryProductResolver:
    unit_of_work: Type[AbstractProductUnitOfWork] = SQLAlchemyProductUnitOfWork

    async def get_list(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[schemas.Product]:
        fields: list[str] = []
        for selected_field in info.selected_fields:
            for field in selected_field.selections:
                fields.append(to_snake_case(field.name))

        uow = self.unit_of_work()
        async with uow:
            products = await uow.products.get_list(*fields, offset=offset, limit=limit)
            await uow.commit()
        return [schemas.Product(**p.model_dump()) for p in products]

    async def get(self, id: int) -> schemas.Product | None:
        uow = self.unit_of_work()
        async with uow:
            product = await uow.products.get(id=id)
            await uow.commit()
        if not product:
            return None
        return schemas.Product(**product.model_dump())
