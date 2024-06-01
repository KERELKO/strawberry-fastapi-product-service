import strawberry
from strawberry.types.nodes import Selection

from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.di import Container
from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.graphql import parse_id
from src.products.dto import ProductDTO
from src.products.graphql.schemas.products.inputs import ProductInput, UpdateProductInput
from src.products.graphql.schemas.products.queries import DeletedProduct, Product
from src.products.repositories.base import AbstractProductUnitOfWork


class StrawberryProductResolver(BaseStrawberryResolver):
    @classmethod
    async def get_list(
        cls,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        required_fields = await cls._fields_to_string(fields)
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            products = await uow.products.get_list(
                fields=required_fields, offset=offset, limit=limit,
            )
            await uow.commit()
        return [Product(**p.model_dump()) for p in products]

    @classmethod
    async def get(cls, id: strawberry.ID, fields: list[Selection]) -> Product | None:
        required_fields = await cls._fields_to_string(fields)
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            try:
                product = await uow.products.get(fields=required_fields, id=parse_id(id))
            except ObjectDoesNotExistException:
                return None
            await uow.commit()
        return Product(**product.model_dump())

    @classmethod
    async def get_by_review_id(
        cls,
        review_id: strawberry.ID,
        fields: list[Selection],
    ) -> Product | None:
        required_fields = await cls._fields_to_string(fields)
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            try:
                product = await uow.products.get_by_review_id(
                    fields=required_fields, review_id=parse_id(review_id),
                )
            except ObjectDoesNotExistException:
                return None
            await uow.commit()
        return Product(**product.model_dump())

    @classmethod
    async def create(cls, input: ProductInput) -> Product:
        dto = ProductDTO(**strawberry.asdict(input))
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            new_product: ProductDTO = await uow.products.create(dto=dto)
        return Product(**new_product.model_dump())

    @classmethod
    async def update(cls, id: strawberry.ID, input: UpdateProductInput) -> Product:
        dto = ProductDTO(**strawberry.asdict(input))
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            updated_product: ProductDTO = await uow.products.update(dto=dto, id=parse_id(id))
            await uow.commit()
        return Product(**updated_product.model_dump())

    @classmethod
    async def delete(cls, id: strawberry.ID) -> DeletedProduct:
        uow = Container.resolve(AbstractProductUnitOfWork)
        async with uow:
            is_deleted = await uow.products.delete(id=parse_id(id))
            await uow.commit()
        return DeletedProduct(success=is_deleted, id=parse_id(id))
