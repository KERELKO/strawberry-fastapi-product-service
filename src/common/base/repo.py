from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.common.base.dto import ID


T = TypeVar('T')


class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def get(self, id: ID, fields: list[str]) -> T:
        ...

    @abstractmethod
    async def get_list(self, fields: list[str], offset: int = 0, limit: int = 20) -> list[T]:
        ...

    @abstractmethod
    async def create(self, dto: T) -> T:
        ...

    @abstractmethod
    async def update(self, id: ID, dto: T) -> T:
        ...

    @abstractmethod
    async def delete(self, id: ID) -> bool:
        ...
