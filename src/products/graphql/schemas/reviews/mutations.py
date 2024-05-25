import strawberry

from src.common.base.graphql.schemas import IReview
from src.common.exceptions import ObjectDoesNotExistException
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.schemas.reviews.inputs import ReviewInput, UpdateReviewInput
from src.products.graphql.schemas.reviews.queries import DeletedReview


@strawberry.type
class ReviewMutations:
    @strawberry.mutation
    async def add_review(self, input: ReviewInput) -> IReview:
        new_review = await StrawberryReviewResolver.create(input=input)
        return new_review

    @strawberry.mutation
    async def update_review(self, input: UpdateReviewInput, id: int) -> IReview:
        updated_review = await StrawberryReviewResolver.update(input=input, id=id)
        return updated_review

    @strawberry.mutation
    async def delete_review(self, id: strawberry.ID) -> DeletedReview:
        try:
            deleted: DeletedReview = await StrawberryReviewResolver.delete(id=int(id))
        except ObjectDoesNotExistException:
            deleted.message = 'Review was not deleted'
            return deleted
        return deleted
