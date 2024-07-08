from dataclasses import dataclass

import strawberry
from strawberry.types.nodes import Selection

from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.utils.graphql import parse_id
from src.products.dto import ProductDTO
from src.products.graphql.schemas.products.inputs import ProductInput, UpdateProductInput
from src.products.graphql.schemas.products.queries import DeletedProduct, Product
from src.products.services.products import ProductService


@dataclass(eq=False, repr=False)
class StrawberryProductResolver(BaseStrawberryResolver):
    service: ProductService

    async def get_list(
        self,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        required_fields = self._selections_to_strings(fields)
        products = await self.service.get_products_list(
            fields=required_fields, offset=offset, limit=limit,
        )
        return [Product(**p.model_dump()) for p in products]

    async def get(self, id: strawberry.ID, fields: list[Selection]) -> Product | None:
        required_fields = self._selections_to_selected_fields(fields)
        product = await self.service.get_product_by_id(id=parse_id(id), fields=required_fields)
        return Product(**product.model_dump())

    async def get_by_review_id(
        self,
        review_id: strawberry.ID,
        fields: list[Selection],
    ) -> Product | None:
        required_fields = self._selections_to_selected_fields(fields)
        product = await self.service.get_by_review_id(review_id=review_id, fields=required_fields)
        return Product(**product.model_dump())

    async def create(self, input: ProductInput) -> Product:
        dto = ProductDTO(**strawberry.asdict(input))
        new_product = await self.service_create_product(dto=dto)
        return Product(**new_product.model_dump())

    async def update(self, id: strawberry.ID, input: UpdateProductInput) -> Product:
        dto = ProductDTO(**strawberry.asdict(input))
        updated_product = await self.service.update_product(id=parse_id(id), dto=dto)
        return Product(**updated_product.model_dump())

    async def delete(self, id: strawberry.ID) -> DeletedProduct:
        is_deleted = await self.service.delete_product(id=parse_id(id))
        return DeletedProduct(success=is_deleted, id=parse_id(id))
