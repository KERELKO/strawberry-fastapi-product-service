from strawberry.utils.str_converters import to_snake_case
from strawberry.types.nodes import Selection

from src.common.di import Container
from src.users.graphql import schemas
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserUnitOfWork


class StrawberryUserResolver:
    @classmethod
    async def _get_list_fields(cls, fields: list[Selection]) -> list[str]:
        list_fields: list[str] = []
        for field in fields:
            list_fields.append(to_snake_case(field.name))
        return list_fields

    @classmethod
    async def get_list(
        cls,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[schemas.User]:
        required_fields: list[str] = await StrawberryUserResolver._get_list_fields(fields=fields)
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            users: list[UserDTO] = await uow.users.get_list(
                fields=required_fields, offset=offset, limit=limit,
            )
            await uow.commit()
        return [schemas.User(**user.model_dump()) for user in users]

    @classmethod
    async def get(
        cls,
        id: int,
        fields: list[Selection],
    ) -> schemas.User | None:
        uow = Container.resolve(AbstractUserUnitOfWork)
        required_fields: list[str] = await StrawberryUserResolver._get_list_fields(fields=fields)
        async with uow:
            user: UserDTO = await uow.users.get(id=id, fields=required_fields)
            await uow.commit()
        if not user:
            return None
        return schemas.User(**user.model_dump())
