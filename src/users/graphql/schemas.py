import strawberry

from src.common.base.graphql.schemas import IUser
from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.common.base.graphql.schemas import IReview


@strawberry.type
class User(IUser):
    id: strawberry.ID
    username: str

    @strawberry.field
    def reviews(self, info: strawberry.Info, offset: int = 0, limit: int = 20) -> list[IReview]:
        if not self.id:
            return []
        fields = get_required_fields(info)
        reviews = StrawberryReviewResolver.get_list(
            fields=fields, user_id=self.id, offset=offset, limit=limit,
        )
        return reviews
