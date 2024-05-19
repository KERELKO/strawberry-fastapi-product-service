from typing import Any
from sqlalchemy import Select, select
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.common.db.sqlalchemy.models import Review, User
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserRepository

from .exceptions import NoUserIDException


class SQLAlchemyUserRepository(BaseSQLAlchemyRepository, AbstractUserRepository):
    async def _join_reviews(
        self,
        fields_to_select: list[InstrumentedAttribute],
        review_fields: list[str],
        user_id: int = None,
    ) -> Select:
        fields_to_select.extend([getattr(Review, f) for f in review_fields])
        if not user_id:
            raise NoUserIDException()
        stmt = select(*fields_to_select).join(Review, onclause=user_id == Review.user_id)
        return stmt

    async def _construct_query(
        self,
        user_fields: list[str],
        review_fields: list[str],
        **queries,
    ) -> Select:
        user_id = queries.get('id', None)
        fields_to_select = [getattr(User, f) for f in user_fields]
        if review_fields:
            stmt = await self._join_reviews(
                fields_to_select=fields_to_select,
                review_fields=review_fields,
                user_id=user_id,
            )
        else:
            stmt = select(*fields_to_select)
        if user_id is not None:
            stmt = stmt.where(User.id == user_id)
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
        user_fields: list[str],
        review_fields: list[str] = None,
        **queries,
    ) -> list[tuple[Any]]:
        stmt = await self._construct_query(
            user_fields=user_fields, review_fields=review_fields, **queries,
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        list_values = await self._execute_query(user_fields=fields, offset=offset, limit=limit)
        dtos = []
        for values in list_values:
            data = {field: value for field, value in zip(fields, values)}
            dtos.append(UserDTO(**data))
        return dtos

    async def get(
        self,
        id: int,
        user_fields: list[str],
        review_fields: list[str] = None,
    ) -> UserDTO | None:
        list_values = await self._execute_query(
            user_fields=user_fields, review_fields=review_fields, id=id,
        )
        values = list_values[0]
        data = {}
        for value_index, field in enumerate(user_fields):
            data[field] = values[value_index]
        return UserDTO(**data)
