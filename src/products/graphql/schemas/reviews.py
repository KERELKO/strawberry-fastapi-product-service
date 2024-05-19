import strawberry


@strawberry.type
class Review:
    id: strawberry.ID
    text: str
