from strawberry.utils.str_converters import to_snake_case
from strawberry.types.nodes import Selection

from src.common.di import Container
from src.products.graphql.schemas.products import Product
from src.products.repositories.base import AbstractProductUnitOfWork


class StrawberryProductResolver:
    @classmethod
    async def _get_list_fields(cls, fields: list[Selection]) -> list[str]:
        list_fields: list[str] = []
        for field in fields:
            list_fields.append(to_snake_case(field.name))
        return list_fields

    @classmethod
    async def get_list(
        cls,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        required_fields = await cls._get_list_fields(fields)
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            products = await uow.products.get_list(
                fields=required_fields, offset=offset, limit=limit,
            )
            await uow.commit()
        return [Product(**p.model_dump()) for p in products]

    @classmethod
    async def get(cls, id: int, fields: list[Selection]) -> Product | None:
        required_fields = await cls._get_list_fields(fields)
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            product = await uow.products.get(fields=required_fields, id=id)
            await uow.commit()
        if not product:
            return None
        return Product(**product.model_dump())

    @classmethod
    async def get_by_review_id(cls, review_id: int, fields: list[Selection]) -> Product:
        required_fields = await cls._get_list_fields(fields)
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            product = await uow.products.get_by_review_id(
                fields=required_fields, review_id=review_id,
            )
            await uow.commit()
        return Product(**product.model_dump())
