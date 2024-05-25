from typing import Any
from sqlalchemy import Select, select

from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.common.db.sqlalchemy.models import Product, Review
from src.products.dto import ProductDTO
from src.common.exceptions import ObjectDoesNotExistException


class SQLAlchemyProductRepository(BaseSQLAlchemyRepository):
    class Meta:
        model = Product

    async def _join_reviews(self, stmt: Select) -> Select:
        stmt = stmt.join(Review, onclause=Product.id == Review.product_id)
        return stmt

    async def _construct_query(
        self,
        fields: list[str],
        **queries,
    ) -> Select:
        product_id = queries.get('id', None)
        review_id = queries.get('review_id', None)
        fields_to_select = [getattr(Product, f) for f in fields]
        offset = queries.get('offset', None)
        limit = queries.get('limit', None)
        stmt = select(*fields_to_select)

        if product_id is not None:
            stmt = stmt.where(Product.id == product_id)
        elif review_id is not None:
            stmt = await self._join_reviews(stmt)
            stmt = stmt.where(Review.id == review_id)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        return stmt

    async def _execute_query(self, *args, **kwargs) -> list[tuple[Any]]:
        stmt = await self._construct_query(*args, **kwargs)
        result = await self.session.execute(stmt)
        return result.all()

    async def get(self, id: int, fields: list[str]) -> ProductDTO:
        list_values = await self._execute_query(fields=fields, id=id)
        try:
            values = list_values[0]
        except IndexError:
            raise ObjectDoesNotExistException('Product', object_id=id)
        data = {f: v for f, v in zip(fields, values)}
        return ProductDTO(**data)

    async def get_by_review_id(self, review_id: int, fields: list[str]) -> ProductDTO:
        list_values = await self._execute_query(fields=fields, review_id=review_id)
        try:
            values = list_values[0]
        except IndexError:
            raise ObjectDoesNotExistException('Product')
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
