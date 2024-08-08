from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.fields import SelectedFields
from src.products.dto import ProductDTO
from src.products.repositories.base import AbstractProductUnitOfWork


class ProductService:
    def _get_uow(self) -> AbstractProductUnitOfWork:
        from src.common.di import Container
        uow: AbstractProductUnitOfWork = Container.resolve(AbstractProductUnitOfWork)
        return uow

    async def get_product_by_id(self, id: int, fields: list[SelectedFields]) -> ProductDTO | None:
        uow = self._get_uow()
        async with uow:
            try:
                product = await uow.products.get(
                    fields=fields, id=id
                )
            except ObjectDoesNotExistException:
                product = None
        return product

    async def get_products_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        uow = self._get_uow()
        async with uow:
            products = await uow.products.get_list(
                fields=fields, offset=offset, limit=limit,
            )
            await uow.commit()
        return products

    async def get_by_review_id(
        self,
        review_id: int,
        fields: list[SelectedFields],
    ) -> ProductDTO | None:
        uow = self._get_uow()
        async with uow:
            try:
                product = await uow.products.get_by_review_id(
                    fields=fields, review_id=review_id,
                )
            except ObjectDoesNotExistException:
                product = None
            await uow.commit()
        return product

    async def create_product(self, dto: ProductDTO) -> ProductDTO:
        uow = self._get_uow()
        async with uow:
            new_product: ProductDTO = await uow.products.create(dto=dto)
            await uow.commit()
        return new_product

    async def update_product(self, id: int, dto: ProductDTO) -> ProductDTO | None:
        uow = self._get_uow()
        async with uow:
            try:
                updated_product: ProductDTO | None = await uow.products.update(dto=dto, id=id)
            except ObjectDoesNotExistException:
                updated_product = None
            await uow.commit()
        return updated_product

    async def delete_product(self, id: int) -> bool:
        uow = self._get_uow()
        async with uow:
            is_deleted = await uow.products.delete(id=id)
            await uow.commit()
        return is_deleted
