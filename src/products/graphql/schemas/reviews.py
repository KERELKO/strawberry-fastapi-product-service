import strawberry

from src.common.base.graphql.schemas import IProduct, IReview, IUser
from src.common.utils.graphql import get_required_fields


@strawberry.type
class Review(IReview):
    id: strawberry.ID
    content: str
    user_id: strawberry.ID
    product_id: strawberry.ID

    @strawberry.field
    async def product(self, info: strawberry.Info) -> IProduct | None:
        from src.products.graphql.resolvers.products import StrawberryProductResolver
        required_fields = get_required_fields(info)
        if not self.product_id:
            return None
        product = await StrawberryProductResolver.get(id=self.product_id, fields=required_fields)
        return product

    @strawberry.field
    async def user(self, info: strawberry.Info) -> IUser | None:
        from src.users.graphql.resolver import StrawberryUserResolver
        required_fields = get_required_fields(info)
        if not self.user_id:
            return None
        user = await StrawberryUserResolver.get(id=self.user_id, fields=required_fields)
        return user
