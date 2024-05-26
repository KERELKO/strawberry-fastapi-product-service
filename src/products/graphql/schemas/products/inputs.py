from typing import Any

import strawberry


@strawberry.input
class ProductInput:
    title: str
    description: str

    def to_dict(self) -> dict[str, Any]:
        data = {
            'title': self.title,
            'description': self.description,
        }
        return data


@strawberry.input
class UpdateProductInput:
    title: str
    description: str

    def to_dict(self) -> dict[str, Any]:
        data = {
            'title': self.title,
            'description': self.description,
        }
        return data
