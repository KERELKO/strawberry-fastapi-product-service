from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> None:
        ...

    async def __aexit__(self, *args) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...
