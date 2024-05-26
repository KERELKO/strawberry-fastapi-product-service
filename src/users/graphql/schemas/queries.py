import strawberry
import strawberry.mutation

from src.common.base.graphql.schemas import IDeleted, IUser
from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.schemas.reviews.queries import Review


@strawberry.type
class User(IUser):
    id: strawberry.ID
    username: str

    @strawberry.field
    async def reviews(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Review]:
        if not self.id:
            return []
        fields = get_required_fields(info)
        reviews = await StrawberryReviewResolver.get_list(
            fields=fields, user_id=int(self.id), offset=offset, limit=limit,
        )
        return reviews


@strawberry.type
class DeletedUser(IDeleted):
    success: bool
    id: strawberry.ID
    message: str | None = None
