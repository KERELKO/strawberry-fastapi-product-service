from typing import Any
from sqlalchemy import select

from src.common.db.sqlalchemy.models import User
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserRepository


class SQLAlchemyUserRepository(BaseSQLAlchemyRepository, AbstractUserRepository):
    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        fields_to_select = [getattr(User, f) for f in fields]
        stmt = select(*fields_to_select).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        list_values: list[tuple[Any]] = result.all()
        dtos = []
        for values in list_values:
            data = {field: value for field, value in zip(fields, values)}
            dtos.append(UserDTO(**data))
        return dtos

    async def get(self, id: int, fields: list[str]) -> UserDTO | None:
        fields_to_select = [getattr(User, f) for f in fields]
        stmt = select(*fields_to_select).where(User.id == id)
        result = await self.session.execute(stmt)
        values = result.first()
        data = {}
        for i, field in enumerate(fields):
            data[field] = values[i]
        return UserDTO(**data)
