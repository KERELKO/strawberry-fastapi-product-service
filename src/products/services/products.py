from dataclasses import dataclass

from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.fields import SelectedFields
from src.products.dto import ProductDTO
from src.products.repositories.base import AbstractProductUnitOfWork


@dataclass(eq=False)
class ProductService:
    uow: AbstractProductUnitOfWork

    async def get_product_by_id(self, id: int, fields: list[SelectedFields]) -> ProductDTO | None:
        async with self.uow:
            try:
                product = await self.uow.products.get(
                    fields=fields, id=id
                )
            except ObjectDoesNotExistException:
                return None
        return product

    async def get_products_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        async with self.uow:
            products = await self.uow.products.get_list(
                fields=fields, offset=offset, limit=limit,
            )
        return products

    async def get_by_review_id(
        self,
        review_id: int,
        fields: list[SelectedFields],
    ) -> ProductDTO | None:
        async with self.uow:
            try:
                product = await self.uow.products.get_by_review_id(
                    fields=fields, review_id=review_id,
                )
            except ObjectDoesNotExistException:
                return None
        return product

    async def create_product(self, dto: ProductDTO) -> ProductDTO:
        async with self.uow:
            new_product: ProductDTO = await self.uow.products.create(dto=dto)
        return new_product

    async def update_product(self, id: int, dto: ProductDTO) -> ProductDTO:
        async with self.uow:
            updated_product: ProductDTO = await self.uow.products.update(dto=dto, id=id)
            await self.uow.commit()
        return updated_product

    async def delete_product(self, id: int) -> bool:
        async with self.uow:
            is_deleted = await self.uow.products.delete(id=id)
            await self.uow.commit()
        return is_deleted
