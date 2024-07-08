from dataclasses import dataclass

from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.fields import SelectedFields
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserUnitOfWork


@dataclass(eq=False, repr=False)
class UserService:
    uow: AbstractUserUnitOfWork

    async def get_user_list(
        self,
        fields: list[SelectedFields],
        offset: int,
        limit: int,
    ) -> list[UserDTO]:
        async with self.uow:
            users: list[UserDTO] = await self.uow.users.get_list(
                fields=fields, offset=offset, limit=limit,
            )
            await self.uow.commit()
        return users

    async def get_user_by_id(
        self,
        id: int,
        fields: list[SelectedFields],
    ) -> UserDTO | None:
        async with self.uow:
            try:
                user: UserDTO = await self.uow.users.get(id=id, fields=fields)
            except ObjectDoesNotExistException:
                user = None
            await self.uow.commit()
        return user

    async def get_user_by_review_id(
        self,
        review_id: int,
        fields: list[SelectedFields],
    ) -> UserDTO | None:
        async with self.uow:
            try:
                user: UserDTO = await self.uow.users.get_by_review_id(
                    review_id=review_id, fields=fields,
                )
            except ObjectDoesNotExistException:
                user = None
            await self.uow.commit()
        return user

    async def create_user(self, dto: UserDTO) -> UserDTO:
        async with self.uow:
            new_user: UserDTO = await self.uow.users.create(dto=dto)
            await self.uow.commit()
        return new_user

    async def update_user(self, id: int, dto: UserDTO) -> UserDTO:
        async with self.uow:
            updated_user: UserDTO = await self.uow.users.update(dto=dto, id=id)
            await self.uow.commit()
        return updated_user

    async def delete_user(self, id: int) -> bool:
        async with self.uow:
            is_deleted = await self.uow.users.delete(id=id)
            await self.uow.commit()
        return is_deleted
