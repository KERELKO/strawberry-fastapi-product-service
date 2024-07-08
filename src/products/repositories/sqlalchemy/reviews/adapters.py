import sqlalchemy as sql
from sqlalchemy.orm import joinedload

from src.common.db.sqlalchemy.models import Review
from src.products.dto import ReviewDTO, ProductDTO
from src.users.dto import UserDTO

from .repo import SQLAlchemyReviewRepository


class SQLAlchemyAggregatedReviewRepository(SQLAlchemyReviewRepository):
    """
    Special adapter that allows to solve N+1 problem
    when retrieve single or mutiple models from the database
    """

    async def _fetch_many_with_related(
        self,
        offset: int,
        limit: int,
        join_user: bool = False,
        join_product: bool = False,
        **filters,
    ) -> list[Review]:
        stmt = sql.select(Review).offset(offset).limit(limit)
        if join_user:
            stmt = stmt.options(joinedload(Review.user))
        if join_product:
            stmt = stmt.options(joinedload(Review.product))
        reviews = await self.session.execute(stmt)
        return reviews.scalars().all()

    async def _fetch_one_with_related(
        self,
        join_user: bool = False,
        join_product: bool = False,
        **filters,
    ) -> Review | None:
        review_id = filters.get('id', None)
        stmt = sql.select(Review)
        if join_user:
            stmt = stmt.options(joinedload(Review.user))
        if join_product:
            stmt = stmt.options(joinedload(Review.product))
        if review_id is not None:
            stmt = stmt.where(Review.id == review_id)
        review = await self.session.execute(stmt)
        return review.scalar_one_or_none()

    async def get(self, id: int, fields: list[str]) -> ReviewDTO | None:
        join_user = True if any(['user' in f for f in fields]) else False
        join_product = True if any(['product' in f for f in fields]) else False
        _review = await self._fetch_one_with_related(
            join_product=join_product, join_user=join_user, id=id,
        )
        if not _review:
            return None
        review = ReviewDTO(**_review.as_dict())
        if join_product:
            product = ProductDTO(**_review.product.as_dict())
            review.product = product
        if join_user:
            user = UserDTO(**_review.user.as_dict())
            review.user = user
        return review

    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
        product_id: int | None = None,
        user_id: int | None = None,
    ) -> list[ReviewDTO]:
        return await super().get_list(fields, offset, limit, product_id, user_id)
