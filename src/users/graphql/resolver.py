from strawberry.utils.str_converters import to_snake_case
from strawberry.types.nodes import Selection

from src.common.di import Container
from src.users.graphql import schemas
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserUnitOfWork


class StrawberryUserResolver:
    @classmethod
    async def _get_list_fields(cls, fields: list[Selection]) -> list[list[str], list[str]]:
        """
        ## Returns list with two lists inside, each of them represents specific fields for an entity
        ### list_fields[0] - list of fields for 'User'
        ### list_fields[1] - list of fields for 'Review'
        """
        list_fields: list[str] = [[], []]
        for field in fields:
            if field.selections:
                for review_field in field.selections:
                    list_fields[1].append(to_snake_case(review_field.name))
            else:
                list_fields[0].append(to_snake_case(field.name))
        return list_fields

    @classmethod
    async def get_list(
        cls,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[schemas.User]:
        required_fields: list[str] = await StrawberryUserResolver._get_list_fields(fields=fields)
        user_fields = required_fields[0]
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            users: list[UserDTO] = await uow.users.get_list(
                fields=user_fields, offset=offset, limit=limit,
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
        user_fields, review_fields = await StrawberryUserResolver._get_list_fields(fields=fields)
        async with uow:
            user: UserDTO = await uow.users.get(
                id=id, user_fields=user_fields, review_fields=review_fields,
            )
            await uow.commit()
        if not user:
            return None
        return schemas.User(**user.model_dump())
