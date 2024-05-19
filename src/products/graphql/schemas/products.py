import strawberry

from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.schemas.reviews import Review


@strawberry.type
class Product:
    id: strawberry.ID
    title: str
    description: str

    @strawberry.field
    def reviews(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Review]:
        if not self.id:
            return []
        fields = get_required_fields(info)
        reviews = StrawberryReviewResolver.get_list(
            fields=fields, product_id=self.id, offset=offset, limit=limit,
        )
        return reviews
