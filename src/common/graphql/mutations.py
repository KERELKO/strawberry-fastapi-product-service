import strawberry

from src.products.graphql.schemas.products.mutations import ProductMutations
from src.products.graphql.schemas.reviews.mutations import ReviewMutations
from src.users.graphql.schemas.mutations import UserMutations


@strawberry.type
class Mutation:
    @strawberry.field
    def user(self) -> UserMutations:
        return UserMutations()

    @strawberry.field
    def product(self) -> ProductMutations:
        return ProductMutations()

    @strawberry.field
    def review(self) -> ReviewMutations:
        return ReviewMutations()
