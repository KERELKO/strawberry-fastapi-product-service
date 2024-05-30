from abc import ABC
from typing import TypeVar, Generic


T = TypeVar('T')


class AbstractRepository(Generic[T], ABC):
    async def get(self, id: int, fields: list[str]) -> T:
        raise NotImplementedError

    async def get_list(self, fields: list[str], offset: int = 0, limit: int = 20) -> list[T]:
        raise NotImplementedError

    async def create(self, dto: T) -> T:
        raise NotImplementedError

    async def update(self, id: int, dto: T) -> T:
        raise NotImplementedError

    async def delete(self, id: int) -> bool:
        raise NotImplementedError
