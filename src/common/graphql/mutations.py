import strawberry

from src.products.graphql.schemas.products.mutations import ProductMutations
from src.products.graphql.schemas.reviews.mutations import ReviewMutations
from src.users.graphql.schemas.mutations import UserMutations


@strawberry.type
class Mutation:
    @strawberry.field
    def users(self) -> UserMutations:
        return UserMutations()

    @strawberry.field
    def products(self) -> ProductMutations:
        return ProductMutations()

    @strawberry.field
    def reviews(self) -> ReviewMutations:
        return ReviewMutations()
