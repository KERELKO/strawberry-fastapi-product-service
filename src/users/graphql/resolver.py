from strawberry.utils.str_converters import to_snake_case
from strawberry.types.nodes import Selection

from src.common.di import Container
from src.users.graphql.schemas import User
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
    ) -> list[User]:
        required_fields: list[str] = await StrawberryUserResolver._get_list_fields(fields=fields)
        user_fields = required_fields[0]
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            users: list[UserDTO] = await uow.users.get_list(
                fields=user_fields, offset=offset, limit=limit,
            )
            await uow.commit()
        return [User(**user.model_dump()) for user in users]

    @classmethod
    async def get(
        cls,
        id: int,
        fields: list[Selection],
    ) -> User | None:
        uow = Container.resolve(AbstractUserUnitOfWork)
        user_fields = await StrawberryUserResolver._get_list_fields(fields=fields)
        async with uow:
            user: UserDTO = await uow.users.get(id=id, user_fields=user_fields)
            await uow.commit()
        if not user:
            return None
        return User(**user.model_dump())
