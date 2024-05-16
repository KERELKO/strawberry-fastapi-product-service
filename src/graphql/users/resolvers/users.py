import strawberry
from src.graphql.users.schemas import UserType

from .base import AbstractUserResolver


class FakeUserResolver(AbstractUserResolver):
    users: list[UserType] = [
        UserType(id=1, first_name='Luka', last_name='Daunik'),
        UserType(id=2, first_name='Artorias', last_name='Googles'),
        UserType(id=3, first_name='Test FirstName', last_name='Test LastName')
    ]

    @classmethod
    def get_all(cls, parent: strawberry.Parent[UserType]) -> list[UserType]:
        return cls.users

    @classmethod
    def get(cls, id: int, parent: strawberry.Parent[UserType]) -> UserType | None:
        print(parent)
        for user in cls.users:
            if user.id == id:
                return user
        return None
