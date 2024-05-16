import strawberry


@strawberry.type
class UserType:
    id: strawberry.ID
    first_name: str
    last_name: str
