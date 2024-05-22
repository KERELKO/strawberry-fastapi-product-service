from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.common.db.sqlalchemy.models import Review, User
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.common.exceptions import ObjectDoesNotExistException
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserRepository


class SQLAlchemyUserRepository(BaseSQLAlchemyRepository, AbstractUserRepository):
    async def _get_model_fields(
        self,
        user_fields: list[str],
    ) -> tuple[list[InstrumentedAttribute]]:
        user_fields = [getattr(User, f) for f in user_fields]
        return user_fields

    async def _join_reviews(self, stmt: Select) -> Select:
        stmt = stmt.join(Review, onclause=User.id == Review.user_id)
        return stmt

    async def _construct_select_query(
        self,
        user_fields: list[str],
        **queries,
    ) -> Select:
        user_id = queries.get('id', None)
        offset = queries.get('offset', None)
        limit = queries.get('limit', None)
        fields_to_select = await self._get_model_fields(user_fields)
        stmt = select(*fields_to_select)

        if user_id is not None:
            stmt = stmt.where(User.id == user_id)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        return stmt

    async def _execute_query(self, *args, first: bool = False, **kwargs) -> list[tuple[Any]]:
        stmt = await self._construct_select_query(*args, **kwargs)
        result = await self.session.execute(stmt)
        if first:
            return result.first()
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
    ) -> UserDTO:
        list_values = await self._execute_query(
            user_fields=user_fields, id=id,
        )
        try:
            values = list_values[0]
        except IndexError:
            raise ObjectDoesNotExistException('User', id)
        data = {}
        for value_index, field in enumerate(user_fields):
            data[field] = values[value_index]
        return UserDTO(**data)

    async def get_by_review_id(self, review_id: int, user_fields: list[str]) -> UserDTO:
        values = await self._execute_query(
            user_fields=user_fields, review_id=review_id, first=True
        )
        if not values:
            raise ObjectDoesNotExistException('User')
        data = {}
        for value_index, field in enumerate(user_fields):
            data[field] = values[value_index]
        return UserDTO(**data)
