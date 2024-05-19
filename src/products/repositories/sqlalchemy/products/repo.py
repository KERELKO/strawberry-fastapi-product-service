from typing import Any
from sqlalchemy import Select, select

from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.common.db.sqlalchemy.models import Product
from src.products.dto import ProductDTO
from src.products.repositories.base import AbstractProductRepository


class SQLAlchemyProductRepository(AbstractProductRepository, BaseSQLAlchemyRepository):
    async def _construct_query(
        self,
        fields: list[str],
        **queries,
    ) -> Select:
        product_id = queries.get('id', None)
        fields_to_select = [getattr(Product, f) for f in fields]
        stmt = select(*fields_to_select)
        if product_id is not None:
            stmt = stmt.where(Product.id == product_id)
            return stmt
        offset = queries.get('offset', None)
        if offset is not None:
            stmt = stmt.offset(offset)
        limit = queries.get('limit', None)
        if limit is not None:
            stmt = stmt.limit(limit)
        return stmt

    async def _execute_query(
        self,
        fields: list[str],
        **queries,
    ) -> list[tuple[Any]]:
        stmt = await self._construct_query(
            fields=fields, **queries,
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get(self, id: int, fields: list[str]) -> ProductDTO | None:
        list_values = await self._execute_query(fields=fields, id=id)
        values = list_values[0]
        if not values:
            return None
        data = {f: v for f, v in zip(fields, values)}
        return ProductDTO(**data)

    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        list_values = await self._execute_query(fields=fields, offset=offset, limit=limit)
        dtos = []
        for values in list_values:
            data = {f: v for f, v in zip(fields, values)}
            dtos.append(ProductDTO(**data))
        return dtos
