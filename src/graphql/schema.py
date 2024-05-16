import strawberry

from src.graphql.users.schemas import UserType

from .users.resolvers.users import FakeUserResolver


@strawberry.type
class Query:
    users: list[UserType] = strawberry.field(resolver=FakeUserResolver.get_all)

    @strawberry.field
    def user(self, id: int, parent: strawberry.Parent[UserType]) -> UserType | None:
        return FakeUserResolver.get(id=id, parent=parent)


schema = strawberry.Schema(Query)
