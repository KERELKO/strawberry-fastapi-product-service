import strawberry


@strawberry.interface
class IUser:
    username: str


@strawberry.interface
class IReview:
    content: str


@strawberry.interface
class IProduct:
    title: str
