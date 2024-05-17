import strawberry


@strawberry.type
class User:
    id: strawberry.ID
    first_name: str
    last_name: str
