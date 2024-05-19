import strawberry
from strawberry.types.nodes import Selection

from src.products.graphql.resolvers.review import StrawberryReviewResolver
from src.products.graphql.schemas import Review
from src.users.graphql.schemas import User
from src.users.graphql.resolver import StrawberryUserResolver


@strawberry.type
class Query:
    @staticmethod
    def required_fields(info: strawberry.Info) -> list[Selection]:
        return [f.selections for f in info.selected_fields][0]

    @strawberry.field
    async def user(self, id: int, info: strawberry.Info) -> User | None:
        user = await StrawberryUserResolver.get(id=id, fields=Query.required_fields(info))
        return user

    @strawberry.field
    async def users(self, info: strawberry.Info, offset: int = 0, limit: int = 20) -> list[User]:
        users: list[User] = await StrawberryUserResolver.get_list(
            fields=Query.required_fields(info),
            offset=offset,
            limit=limit,
        )
        return users

    @strawberry.field
    async def review(self, id: int, info: strawberry.Info) -> Review:
        review = await StrawberryReviewResolver.get(id=id, fields=Query.required_fields(info))
        return review

    @strawberry.field
    async def reviews(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Review]:
        reviews: list[Review] = await StrawberryReviewResolver.get_list(
            fields=Query.required_fields(info),
            offset=offset,
            limit=limit,
        )
        return reviews


schema = strawberry.Schema(Query)
