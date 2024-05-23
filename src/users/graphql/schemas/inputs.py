from typing import Any
import strawberry


@strawberry.input
class UserInput:
    username: str

    def to_dict(self) -> dict[str, Any]:
        data = {'username': self.username}
        return data


@strawberry.input
class UpdateUserInput:
    username: str

    def to_dict(self) -> dict[str, Any]:
        data = {'username': self.username}
        return data
