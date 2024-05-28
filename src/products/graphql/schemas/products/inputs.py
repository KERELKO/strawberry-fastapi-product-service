import strawberry


@strawberry.input
class ProductInput:
    title: str
    description: str


@strawberry.input
class UpdateProductInput:
    title: str
    description: str
