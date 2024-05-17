import strawberry

from src.users.graphql import schemas
from src.users.graphql.resolver import StrawberryUserResolver


@strawberry.type
class Query:
    # Users
    users: list[schemas.User] = strawberry.field(resolver=StrawberryUserResolver().get_list)
    user: schemas.User | None = strawberry.field(resolver=StrawberryUserResolver().get)
    # Products


schema = strawberry.Schema(Query)
