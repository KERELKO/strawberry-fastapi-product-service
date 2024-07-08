from dataclasses import dataclass

import strawberry
from strawberry.types.nodes import Selection

from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.utils.fields import SelectedFields
from src.common.utils.graphql import parse_id
from src.users.graphql.schemas.inputs import UserInput, UpdateUserInput
from src.users.graphql.schemas.queries import User
from src.users.dto import UserDTO
from src.users.service import UserService


@dataclass(eq=False, repr=False)
class StrawberryUserResolver(BaseStrawberryResolver):
    service: UserService

    async def get_list(
        self,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]:
        required_fields: list[SelectedFields] = self._selections_to_selected_fields(fields=fields)
        users = await self.service.get_user_list(fields=required_fields, offset=offset, limit=limit)
        return [User(**user.model_dump()) for user in users]

    async def get(
        self,
        id: strawberry.ID,
        fields: list[Selection],
    ) -> User | None:
        required_fields = self._selections_to_selected_fields(fields=fields)
        user = await self.service.get_user_by_id(self, id=parse_id(id), fields=required_fields)
        return User(**user.model_dump())

    async def get_by_review_id(
        self,
        review_id: strawberry.ID,
        fields: list[Selection],
    ) -> User | None:
        required_fields = self._selections_to_selected_fields(fields=fields)
        user = await self.service.get_user_by_review_id(
            review_id=parse_id(review_id), fields=required_fields,
        )
        return User(**user.model_dump())

    async def create(self, input: UserInput) -> User:
        dto = UserDTO(**strawberry.asdict(input))
        new_user = await self.service.create_user(dto=dto)
        return User(**new_user.model_dump())

    async def update(self, id: strawberry.ID, input: UpdateUserInput) -> User:
        dto = UserDTO(**strawberry.asdict(input))
        updated_user = await self.service.update_user(id=parse_id(id), dto=dto)
        return User(**updated_user.model_dump())

    async def delete(self, id: strawberry.ID) -> bool:
        return await self.service.delete_user(id=parse_id(id))
