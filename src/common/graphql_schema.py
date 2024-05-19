import strawberry

from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.review import StrawberryReviewResolver
from src.products.graphql.schemas import Review
from src.users.graphql.schemas import User
from src.users.graphql.resolver import StrawberryUserResolver


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int, info: strawberry.Info) -> User | None:
        user = await StrawberryUserResolver.get(id=id, fields=get_required_fields(info))
        return user

    @strawberry.field
    async def users(self, info: strawberry.Info, offset: int = 0, limit: int = 20) -> list[User]:
        users: list[User] = await StrawberryUserResolver.get_list(
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
    ) -> list[Review]:
        reviews: list[Review] = await StrawberryReviewResolver.get_list(
            fields=get_required_fields(info),
            offset=offset,
            limit=limit,
        )
        return reviews


schema = strawberry.Schema(Query)
