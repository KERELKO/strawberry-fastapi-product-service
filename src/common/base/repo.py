from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar('T')


class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def get(self, id: int, fields: list[str]) -> T | None:
        ...

    @abstractmethod
    async def get_list(self, fields: list[str], offset: int = 0, limit: int = 20) -> list[T]:
        ...