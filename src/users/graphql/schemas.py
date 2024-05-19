import strawberry

from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.review import StrawberryReviewResolver
from src.products.graphql.schemas import Review


# TODO: Add checking user.id not only on self, but in query params also
@strawberry.type
class User:
    id: strawberry.ID
    first_name: str
    last_name: str

    # TODO: To provide ability to set "reviews" in __init__ of the class
    @strawberry.field
    def reviews(self, info: strawberry.Info, offset: int = 0, limit: int = 20) -> list[Review]:
        if not self.id:
            return []
        fields = get_required_fields(info)
        reviews = StrawberryReviewResolver.get_list(
            fields=fields, user_id=self.id, offset=offset, limit=limit,
        )
        return reviews
