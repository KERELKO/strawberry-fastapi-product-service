from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from src.common.base.dto import ID
from src.common.exceptions import ObjectDoesNotExistException
from src.users.dto import UserDTO
from src.common.settings import config
from src.users.repositories.base import AbstractUserRepository


class MongoUserRepository(AbstractUserRepository):
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(config.mongo_connection_string)
        self.db = self.client[config.MONGO_DB]
        self.collection = self.db['users']

    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        users: list[UserDTO] = []
        async for user_data in self.collection.find():
            user_data['id'] = str(user_data.pop('_id'))
            users.append(UserDTO(**user_data))
        return users

    async def get(
        self,
        id: ID,
        fields: list[str],
    ) -> UserDTO:
        result = await self.collection.find_one({'_id': ObjectId(oid=str(id))})
        if result:
            data = {f: v for f, v in result.items() if f in fields}
            data['id'] = id
            return UserDTO(**data)
        raise ObjectDoesNotExistException('User', object_id=id)

    async def get_by_review_id(self, review_id: ID, fields: list[str]) -> UserDTO:
        ...

    async def create(self, dto: UserDTO) -> UserDTO:
        data = dto.model_dump()
        result = await self.collection.insert_one(data)
        dto.id = result.inserted_id
        return dto

    async def update(self, id: ID, dto: UserDTO) -> UserDTO:
        ...

    async def delete(self, id: ID) -> bool:
        ...
