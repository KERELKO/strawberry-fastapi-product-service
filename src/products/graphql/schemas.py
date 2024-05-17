import strawberry


@strawberry.type
class Product:
    id: strawberry.ID
    title: str
    description: str


@strawberry.type
class Review:
    id: strawberry.ID
    text: str
