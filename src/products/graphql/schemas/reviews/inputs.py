from typing import Any
import strawberry


@strawberry.input
class ReviewInput:
    content: str
    user_id: int
    product_id: int

    def to_dict(self) -> dict[str, Any]:
        data = {
            'content': self.content,
            'user_id': self.user_id,
            'product_id': self.product_id,
        }
        return data


@strawberry.input
class UpdateReviewInput:
    content: str

    def to_dict(self) -> dict[str, Any]:
        data = {
            'content': self.content,
        }
        return data
