from strawberry.types.nodes import Selection

from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.di import Container
from src.users.graphql.schemas.inputs import UserInput, UpdateUserInput
from src.users.graphql.schemas.query import User
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
        required_fields: list[str] = await cls._get_list_fields(fields=fields)
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            users: list[UserDTO] = await uow.users.get_list(
                fields=required_fields, offset=offset, limit=limit,
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
        user_fields = await cls._get_list_fields(fields=fields)
        async with uow:
            user: UserDTO = await uow.users.get(id=id, user_fields=user_fields)
            await uow.commit()
        return User(**user.model_dump())

    @classmethod
    async def get_by_review_id(cls, review_id: int, fields: list[Selection]) -> User:
        uow = Container.resolve(AbstractUserUnitOfWork)
        user_fields = await cls._get_list_fields(fields=fields)
        async with uow:
            user: UserDTO = await uow.users.get_by_review_id(
                review_id=review_id, user_fields=user_fields,
            )
            await uow.commit()
        return User(**user.model_dump())

    @classmethod
    async def create(cls, input: UserInput) -> User:
        dto = UserDTO(**input.to_dict())
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            new_user: UserDTO = await uow.users.create(dto=dto)
        return User(**new_user.model_dump())

    @classmethod
    async def update(cls, id: int, input: UpdateUserInput) -> User:
        dto = UserDTO(**input.to_dict())
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            updated_user: UserDTO = await uow.users.update(dto=dto, id=id)
            await uow.commit()
        return User(**updated_user.model_dump())

    @classmethod
    async def delete(cls, id: int) -> bool:
        uow = Container.resolve(AbstractUserUnitOfWork)
        async with uow:
            try:
                is_deleted = await uow.users.delete(id=id)
            except Exception as e:
                print(e)
                return False
            await uow.commit()
        return is_deleted
