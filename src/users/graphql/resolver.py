import strawberry
from strawberry.types.nodes import Selection

from src.common.di import Container
from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.graphql import parse_id
from src.users.graphql.schemas.inputs import UserInput, UpdateUserInput
from src.users.graphql.schemas.queries import User
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserUnitOfWork


class StrawberryUserResolver(BaseStrawberryResolver):
    @classmethod
    async def get_list(
        cls,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]:
        required_fields: list[str] = cls._selections_to_strings(fields=fields)
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            users: list[UserDTO] = await uow.users.get_list(
                fields=required_fields, offset=offset, limit=limit,
            )
        return [User(**user.model_dump()) for user in users]

    @classmethod
    async def get(
        cls,
        id: strawberry.ID,
        fields: list[Selection],
    ) -> User | None:
        uow = Container.resolve(AbstractUserUnitOfWork)
        user_fields = cls._selections_to_strings(fields=fields)
        async with uow:
            try:
                user: UserDTO = await uow.users.get(id=parse_id(id), fields=user_fields)
            except ObjectDoesNotExistException:
                return None
        return User(**user.model_dump())

    @classmethod
    async def get_by_review_id(
        cls,
        review_id: strawberry.ID,
        fields: list[Selection],
    ) -> User | None:
        uow = Container.resolve(AbstractUserUnitOfWork)
        user_fields = cls._selections_to_strings(fields=fields)
        async with uow:
            try:
                user: UserDTO = await uow.users.get_by_review_id(
                    review_id=parse_id(review_id), fields=user_fields,
                )
            except ObjectDoesNotExistException:
                return None
        return User(**user.model_dump())

    @classmethod
    async def create(cls, input: UserInput) -> User:
        dto = UserDTO(**strawberry.asdict(input))
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            new_user: UserDTO = await uow.users.create(dto=dto)
        return User(**new_user.model_dump())

    @classmethod
    async def update(cls, id: strawberry.ID, input: UpdateUserInput) -> User:
        dto = UserDTO(**strawberry.asdict(input))
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            updated_user: UserDTO = await uow.users.update(dto=dto, id=parse_id(id))
            await uow.commit()
        return User(**updated_user.model_dump())

    @classmethod
    async def delete(cls, id: strawberry.ID) -> bool:
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            is_deleted = await uow.users.delete(id=parse_id(id))
            await uow.commit()
        return is_deleted
