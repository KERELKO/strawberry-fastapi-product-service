import strawberry

from src.common.base.graphql.schemas import IDeleted, IProduct
from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.schemas.reviews.queries import Review


@strawberry.type
class Product(IProduct):
    id: strawberry.ID
    title: str
    description: str

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
            fields=fields, product_id=int(self.id), offset=offset, limit=limit,
        )
        return reviews


@strawberry.type
class DeletedProduct(IDeleted):
    id: strawberry.ID
    success: bool
    message: str | None = None
