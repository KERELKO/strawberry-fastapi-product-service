from typing import Any

import sqlalchemy as sql
from sqlalchemy.orm import joinedload

from src.common.utils import raise_exc
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.common.db.sqlalchemy.extensions import sqlalchemy_repo_extended, _models_to_join
from src.common.db.sqlalchemy.models import Product, Review
from src.common.utils.fields import SelectedFields
from src.products.dto import ProductDTO, ReviewDTO
from src.common.exceptions import ObjectDoesNotExistException


@sqlalchemy_repo_extended(query_executor=False)
class SQLAlchemyProductRepository(BaseSQLAlchemyRepository):
    class Meta:
        model = Product

    def _construct_select_query(
        self,
        fields: list[SelectedFields],
        **queries,
    ) -> sql.Select:
        product_id = queries.get('id', None)
        review_id = queries.get('review_id', None)
        _fields = fields[0] if len(fields) > 0 else raise_exc(Exception('No fields'))
        fields_to_select = [getattr(Product, f) for f in _fields.fields]
        offset = queries.get('offset', None)
        limit = queries.get('limit', None)
        stmt = sql.select(*fields_to_select)

        if product_id is not None:
            stmt = stmt.where(Product.id == product_id)
        elif review_id is not None:
            stmt = stmt.join(Review)
            stmt = stmt.where(Review.id == review_id)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        return stmt

    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> ProductDTO:
        values = await self._execute_query(fields=fields, review_id=review_id, first=True)
        if not values:
            raise ObjectDoesNotExistException('Product')
        data: dict[str, Any] = {f: v for f, v in zip(fields, values)}
        return ProductDTO(**data)

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        list_values = await self._execute_query(fields=fields, offset=offset, limit=limit)
        dto_list = []
        for values in list_values:
            data = {f: v for f, v in zip(fields, values)}
            dto_list.append(ProductDTO(**data))
        return dto_list


class SQLAlchemyAggregatedProductRepository(SQLAlchemyProductRepository):
    async def _fetch_one_with_related(self, join_reviews: bool, **filters) -> Product | None:
        product_id = filters.get('id', None)
        review_id = filters.get('review_id', None)
        stmt = sql.Select(Product)
        if join_reviews:
            stmt = stmt.options(joinedload(Product.reviews))
        if product_id is not None:
            stmt = stmt.where(Product.id == product_id)
        elif review_id is not None:
            stmt = stmt.join(Product.reviews)
            stmt = stmt.where(Review.id == review_id)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def _fetch_many_with_related(self, join_reviews: bool, **filters) -> list[Product]:
        offset = filters.get('offset', 0)
        limit = filters.get('limit', 20)
        stmt = sql.Select(Product).offset(offset).limit(limit)
        if join_reviews:
            stmt = stmt.options(joinedload(Product.reviews))
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get(self, id: int, fields: list[SelectedFields]) -> ProductDTO:
        _, _, join_review = _models_to_join(fields)
        _product = await self._fetch_one_with_related(id=id, join_reviews=join_review)
        if not _product:
            raise ObjectDoesNotExistException(Product.__name__, id=id)
        product = ProductDTO(**_product.as_dict())
        if join_review:
            reviews = [ReviewDTO(**r.as_dict()) for r in _product.reviews]
            product.reviews = reviews
        return product

    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> ProductDTO:
        review = self.session.get(Review, id=review_id)
        if not review:
            raise ObjectDoesNotExistException('Review', object_id=review_id)
        return await self.get(id=review.product_id, fields=fields)

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        _, _, join_review = _models_to_join(fields)
        _products = await self._fetch_many_with_related(
            offset=offset, limit=limit, join_reviews=join_review,
        )
        products: list[ProductDTO] = []
        for _product in _products:
            product = ProductDTO(**_product.as_dict())
            if join_review:
                reviews = [ReviewDTO(**r.as_dict()) for r in _product.reviews]
                product.reviews = reviews
            products.append(product)
        return products
