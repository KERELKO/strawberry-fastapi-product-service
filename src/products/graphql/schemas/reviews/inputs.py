import strawberry


@strawberry.input
class ReviewInput:
    content: str
    user_id: int
    product_id: int


@strawberry.input
class UpdateReviewInput:
    content: str
