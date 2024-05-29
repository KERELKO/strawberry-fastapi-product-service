import strawberry


@strawberry.input
class ReviewInput:
    content: str
    user_id: strawberry.ID
    product_id: strawberry.ID


@strawberry.input
class UpdateReviewInput:
    content: str
