import strawberry

from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.resolvers.products import StrawberryProductResolver
from src.products.graphql.schemas.products import Product
from src.products.graphql.schemas.reviews import Review
from src.users.graphql.resolver import StrawberryUserResolver
from src.users.graphql.schemas.query import User


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID, info: strawberry.Info) -> User | None:
        user = await StrawberryUserResolver.get(id=int(id), fields=get_required_fields(info))
        return user

    @strawberry.field
    def users(self, info: strawberry.Info, offset: int = 0, limit: int = 20) -> list[User]:
        users: list[User] = StrawberryUserResolver.get_list(
            fields=get_required_fields(info),
            offset=offset,
            limit=limit,
        )
        return users

    @strawberry.field
    async def review(self, id: strawberry.ID, info: strawberry.Info) -> Review:
        review = await StrawberryReviewResolver.get(id=int(id), fields=get_required_fields(info))
        return review

    @strawberry.field
    async def reviews(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Review]:
        reviews: list[Review] = await StrawberryReviewResolver.get_list(
            fields=get_required_fields(info),
            offset=offset,
            limit=limit,
        )
        return reviews

    @strawberry.field
    async def product(self, id: strawberry.ID, info: strawberry.Info) -> Product | None:
        product = await StrawberryProductResolver.get(id=int(id), fields=get_required_fields(info))
        return product

    @strawberry.field
    async def products(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        products: list[Product] = await StrawberryProductResolver.get_list(
            fields=get_required_fields(info),
            offset=offset,
            limit=limit,
        )
        return products
