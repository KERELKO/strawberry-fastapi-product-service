from motor.motor_asyncio import AsyncIOMotorClient

from src.common.exceptions import ObjectDoesNotExistException
from src.users.dto import UserDTO
from src.common.settings import config


class MongoUserRepository:
    primary_key: int = 0

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(config.mongo_connection_string)
        self.db = self.client[config.MONGO_DB]
        self.collection = self.db["users"]

    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        users: list[UserDTO] = []
        async for user in self.collection.find():
            users.append(UserDTO(**user))
        return users

    async def get(
        self,
        id: int,
        fields: list[str],
    ) -> UserDTO:
        result = await self.collection.find_one({'id': id})
        if result:
            return UserDTO(**result)
        raise ObjectDoesNotExistException('User', object_id=id)

    async def get_by_review_id(self, review_id: int, fields: list[str]) -> UserDTO:
        ...

    async def create(self, dto: UserDTO) -> UserDTO:
        data = dto.model_dump()
        data['id'] = self.primary_key
        self.primary_key += 1
        result = await self.collection.insert_one(data)
        dto.id = result.inserted_id
        return dto

    async def update(self, id: int, dto: UserDTO) -> UserDTO:
        ...

    async def delete(self, id: int) -> bool:
        ...
