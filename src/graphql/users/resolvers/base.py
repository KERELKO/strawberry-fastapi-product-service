from abc import ABC, abstractmethod

from src.graphql.users.schemas import UserType


class AbstractUserResolver(ABC):
    @classmethod
    @abstractmethod
    def get_all(cls) -> list[UserType]:
        ...

    @classmethod
    @abstractmethod
    def get(cls, id: int) -> UserType | None:
        ...
