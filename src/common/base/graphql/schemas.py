import strawberry


@strawberry.interface
class IUser:
    id: strawberry.ID
    username: str


@strawberry.interface
class IReview:
    id: strawberry.ID
    content: str
    user_id: strawberry.ID
    product_id: strawberry.ID


@strawberry.interface
class IProduct:
    id: strawberry.ID
    title: str
    description: str
