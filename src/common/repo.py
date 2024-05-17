from abc import ABC, abstractmethod
from typing import TypeVar


T = TypeVar('T')


class AbstractRepository[T](ABC):
    @abstractmethod
    async def get(self, id: int) -> T:
        ...

    @abstractmethod
    async def get_list(self, offset: int = 0, limit: int = 20, **fields) -> list[T]:
        ...
