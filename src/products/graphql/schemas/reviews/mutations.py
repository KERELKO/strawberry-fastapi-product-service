import strawberry

from src.common.base.graphql.schemas import IReview
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.schemas.reviews.inputs import ReviewInput


@strawberry.type
class ReviewMutations:
    @strawberry.mutation
    async def add_review(self, input: ReviewInput) -> IReview:
        new_review = await StrawberryReviewResolver.create(input=input)
        return new_review
