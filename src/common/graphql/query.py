import strawberry

from src.common.di import Container
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.resolvers.products import StrawberryProductResolver
from src.products.graphql.schemas.products.queries import Product
from src.products.graphql.schemas.reviews.queries import Review
from src.users.graphql.resolver import StrawberryUserResolver
from src.users.graphql.schemas.queries import User


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID, info: strawberry.Info) -> User | None:
        resolver = Container.resolve(StrawberryUserResolver)
        user = await resolver.get(id=id, fields=info.selected_fields)
        return user

    @strawberry.field
    async def users(self, info: strawberry.Info, offset: int = 0, limit: int = 20) -> list[User]:
        resolver = Container.resolve(StrawberryUserResolver)
        users: list[User] = await resolver.get_list(
            fields=info.selected_fields,
            offset=offset,
            limit=limit,
        )
        return users

    @strawberry.field
    async def review(self, id: strawberry.ID, info: strawberry.Info) -> Review | None:
        resolver = Container.resolve(StrawberryReviewResolver)
        review = await resolver.get(
            id=id, fields=info.selected_fields,
        )
        return review

    @strawberry.field
    async def reviews(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Review]:
        resolver = Container.resolve(StrawberryReviewResolver)
        reviews: list[Review] = await resolver.get_list(
            fields=info.selected_fields,
            offset=offset,
            limit=limit,
        )
        return reviews

    @strawberry.field
    async def product(self, id: strawberry.ID, info: strawberry.Info) -> Product | None:
        resolver = Container.resolve(StrawberryProductResolver)
        product = await resolver.get(
            id=id, fields=info.selected_fields,
        )
        return product

    @strawberry.field
    async def products(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        resolver = Container.resolve(StrawberryProductResolver)
        products: list[Product] = await resolver.get_list(
            fields=info.selected_fields,
            offset=offset,
            limit=limit,
        )
        return products
