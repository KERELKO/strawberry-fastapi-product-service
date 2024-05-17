import strawberry

from src.products.graphql.resolvers.product import StrawberryProductResolver
from src.products.graphql.resolvers.review import StrawberryReviewResolver
from src.products.graphql.schemas import Product, Review
from src.users.graphql.schemas import User
from src.users.graphql.resolver import StrawberryUserResolver


@strawberry.type
class Query:
    # Users
    users: list[User] = strawberry.field(resolver=StrawberryUserResolver().get_list)
    user: User | None = strawberry.field(resolver=StrawberryUserResolver().get)
    # Products
    product: Product | None = strawberry.field(resolver=StrawberryProductResolver().get)
    products: list[Product] = strawberry.field(resolver=StrawberryProductResolver().get_list)
    # Reviews
    review: Review | None = strawberry.field(resolver=StrawberryReviewResolver().get)
    reviews: list[Review] = strawberry.field(resolver=StrawberryReviewResolver().get_list)


schema = strawberry.Schema(Query)
