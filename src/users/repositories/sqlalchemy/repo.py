import sqlalchemy as sql
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.common.db.sqlalchemy.extensions import sqlalchemy_repo_extended
from src.common.db.sqlalchemy.models import User
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.common.exceptions import ObjectDoesNotExistException
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserRepository


@sqlalchemy_repo_extended(query_executor=False)
class SQLAlchemyUserRepository(AbstractUserRepository, BaseSQLAlchemyRepository):
    class Meta:
        model = User

    async def _construct_select_query(
        self,
        fields: list[str],
        **queries,
    ) -> sql.Select:
        user_id = queries.get('id', None)
        offset = queries.get('offset', None)
        limit = queries.get('limit', None)
        fields_to_select: list[InstrumentedAttribute] = [getattr(User, f) for f in fields]
        stmt = sql.select(*fields_to_select)

        if user_id is not None:
            stmt = stmt.where(User.id == user_id)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        return stmt

    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        list_values = await self._execute_query(fields=fields, offset=offset, limit=limit)
        dtos = []
        for values in list_values:
            data = {field: value for field, value in zip(fields, values)}
            dtos.append(UserDTO(**data))
        return dtos

    async def get(
        self,
        id: int,
        fields: list[str],
    ) -> UserDTO:
        values = await self._execute_query(
            fields=fields, id=id, first=True,
        )
        if not values:
            raise ObjectDoesNotExistException('User', id)
        data = {}
        for value_index, field in enumerate(fields):
            data[field] = values[value_index]
        return UserDTO(**data)

    async def get_by_review_id(self, review_id: int, fields: list[str]) -> UserDTO:
        values = await self._execute_query(
            fields=fields, review_id=review_id, first=True
        )
        if not values:
            raise ObjectDoesNotExistException('User')
        data = {}
        for value_index, field in enumerate(fields):
            data[field] = values[value_index]
        return UserDTO(**data)
