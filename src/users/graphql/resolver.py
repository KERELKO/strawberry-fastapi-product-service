from dataclasses import dataclass

import strawberry
from strawberry.utils.str_converters import to_snake_case

from src.users.graphql import schemas
from src.users.dto import UserDTO
from src.users.repositories.sqlalchemy.uow import SQLAlchemyUserUnitOfWork
from src.users.repositories.base import AbstractUserUnitOfWork


# TODO: remove dependencies
@dataclass
class StrawberryUserResolver:
    unit_of_work: AbstractUserUnitOfWork = SQLAlchemyUserUnitOfWork

    async def get_list(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[schemas.User]:
        fields: list[str] = []
        for selected_field in info.selected_fields:
            for field in selected_field.selections:
                fields.append(to_snake_case(field.name))

        uow = self.unit_of_work()
        async with uow:
            users: list[UserDTO] = await uow.users.get_list(
                *fields, offset=offset, limit=limit,
            )
            await uow.commit()
        return [schemas.User(**user.model_dump()) for user in users]

    async def get(self, id: int) -> schemas.User | None:
        uow = self.unit_of_work()
        async with uow:
            user = await uow.users.get(id=id)
            await uow.commit()
        if not user:
            return None
        return schemas.User(**user.model_dump())
