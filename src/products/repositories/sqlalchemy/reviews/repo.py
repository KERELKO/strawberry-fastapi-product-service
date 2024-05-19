from typing import Any
from sqlalchemy import Select, select

from src.common.db.sqlalchemy.models import Review
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.products.dto import ReviewDTO
from src.products.repositories.base import AbstractReviewRepository


# TODO: Add logger that saves all constructed statements
class SQLAlchemyReviewRepository(AbstractReviewRepository, BaseSQLAlchemyRepository):
    async def _construct_query(self, fields: list[str], **queries) -> Select:
        fields_to_select = [getattr(Review, f) for f in fields]
        stmt = select(*fields_to_select)
        if 'id' in queries:
            return stmt.where(Review.id == queries['id'])
        user_id = queries['user_id']
        product_id = queries['product_id']
        if user_id:
            stmt = stmt.where(Review.user_id == user_id)
        if product_id:
            stmt = stmt.where(Review.product_id == product_id)
        if 'offset' in queries:
            stmt = stmt.offset(queries['offset'])
        if 'limit' in queries:
            stmt = stmt.limit(queries['limit'])
        return stmt

    async def _execute_query(self, fields: list[str], **queries) -> list[tuple[Any]]:
        """
        ## Returns the result.all() of the session.execute(stmt)
        ### order of the values equals to the order of values passed in the 'fields' arg
        ### example:
        ###     if fields = ['id', 'text']
        ###     returns [(1, 'I like bananas'), (2, 'Who is going to give a job?'), ...]
        """
        stmt = await self._construct_query(fields=fields, **queries)
        result = await self.session.execute(stmt)
        return result.all()

    async def get(self, id: int, fields: list[str]) -> ReviewDTO | None:
        list_values = await self._execute_query(fields, id=id)
        values = list_values[0]
        data = {}
        for i, field in enumerate(fields):
            data[field] = values[i]
        return ReviewDTO(**data)

    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
        user_id: int = None,
        product_id: int = None,
    ) -> list[ReviewDTO]:
        list_values = await self._execute_query(
            fields=fields,
            offset=offset,
            limit=limit,
            user_id=user_id,
            product_id=product_id,
        )
        dtos = []
        for values in list_values:
            data = {f: v for f, v in zip(fields, values)}
            dtos.append(ReviewDTO(**data))
        return dtos
