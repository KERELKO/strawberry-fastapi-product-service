import strawberry


@strawberry.input
class UserInput:
    username: str


@strawberry.input
class UpdateUserInput:
    username: str
