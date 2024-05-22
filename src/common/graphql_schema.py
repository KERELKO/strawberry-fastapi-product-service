import strawberry

from src.common.base.graphql.schemas import IProduct, IReview, IUser
from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.resolvers.products import StrawberryProductResolver
from src.products.graphql.schemas.products import Product
from src.products.graphql.schemas.reviews import Review
from src.users.graphql.resolver import StrawberryUserResolver
from src.users.graphql.schemas import User


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int, info: strawberry.Info) -> User | None:
        user = await StrawberryUserResolver.get(id=id, fields=get_required_fields(info))
        return user

    @strawberry.field
    def users(self, info: strawberry.Info, offset: int = 0, limit: int = 20) -> list[IUser]:
        users: list[IUser] = StrawberryUserResolver.get_list(
            fields=get_required_fields(info),
            offset=offset,
            limit=limit,
        )
        return users

    @strawberry.field
    async def review(self, id: int, info: strawberry.Info) -> Review:
        review = await StrawberryReviewResolver.get(id=id, fields=get_required_fields(info))
        return review

    @strawberry.field
    async def reviews(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[IReview]:
        reviews: list[IReview] = await StrawberryReviewResolver.get_list(
            fields=get_required_fields(info),
            offset=offset,
            limit=limit,
        )
        return reviews

    @strawberry.field
    async def product(self, id: int, info: strawberry.Info) -> Product | None:
        product = await StrawberryProductResolver.get(id=id, fields=get_required_fields(info))
        return product

    @strawberry.field
    async def products(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[IProduct]:
        products: list[IProduct] = await StrawberryProductResolver.get_list(
            fields=get_required_fields(info),
            offset=offset,
            limit=limit,
        )
        return products


schema = strawberry.Schema(Query)
