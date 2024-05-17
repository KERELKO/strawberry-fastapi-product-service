from abc import ABC, abstractmethod
from typing import TypeVar


T = TypeVar('T')


class AbstractRepository[T](ABC):
    @abstractmethod
    async def get(self, id: int) -> T | None:
        ...

    @abstractmethod
    async def get_list(self, *fields, offset: int = 0, limit: int = 20) -> list[T]:
        ...
