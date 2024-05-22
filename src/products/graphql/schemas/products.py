import strawberry

from src.common.base.graphql.schemas import IProduct
from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.schemas.reviews import Review


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
            fields=fields, product_id=self.id, offset=offset, limit=limit,
        )
        return reviews


@strawberry.type
class ProductMutations:
    @strawberry.mutation
    def add_product(self) -> IProduct:
        ...
