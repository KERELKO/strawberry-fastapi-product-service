from sqlalchemy import Select, select

from src.common.db.sqlalchemy.models import Review
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.products.dto import ReviewDTO
from src.products.repositories.base import AbstractReviewRepository


# TODO: remove hardcoding in repositories
class SQLAlchemyReviewRepository(AbstractReviewRepository, BaseSQLAlchemyRepository):
    async def _construct_query(self, *fields, **queries) -> Select:
        if not fields:
            stmt = select(Review)
        else:
            fields_to_select = [getattr(Review, f) for f in fields]
            stmt = select(*fields_to_select)
        if 'id' in queries:
            return stmt.where(Review.id == queries['id'])
        if 'user_id' in queries:
            stmt = stmt.where(Review.user_id == queries['user_id'])
        if 'product_id' in queries:
            stmt = stmt.where(Review.product_id == queries['product_id'])
        if 'offset' in queries:
            stmt = stmt.offset(queries['offset'])
        if 'limit' in queries:
            stmt = stmt.limit(queries['limit'])
        return stmt

    async def get(self, id: int, fields: list[str]) -> ReviewDTO | None:
        fields_to_select = [getattr(Review, f) for f in fields]
        stmt = select(*fields_to_select).where(Review.id == id)
        result = await self.session.execute(stmt)
        values = result.first()
        data = {}
        for i, field in enumerate(fields):
            data[field] = values[i]
        return ReviewDTO(**data)

    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ReviewDTO]:
        fields_to_select = [getattr(Review, f) for f in fields]
        stmt = select(*fields_to_select).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        list_values = result.all()
        dtos = []
        for values in list_values:
            data = {f: v for f, v in zip(fields, values)}
            dtos.append(ReviewDTO(**data))
        return dtos
