import strawberry

from src.common.base.graphql.schemas import IDeleted, IProduct, IReview, IUser
from src.common.exceptions import IDIsNotProvided
from src.common.utils.graphql import get_required_fields


@strawberry.type
class Review(IReview):
    id: strawberry.ID
    content: str
    _user_id: strawberry.ID | None = None
    _product_id: strawberry.ID | None = None

    @strawberry.field
    async def product(self, info: strawberry.Info) -> IProduct:
        from src.products.graphql.resolvers.products import StrawberryProductResolver
        required_fields = get_required_fields(info)
        if not self.id:
            raise IDIsNotProvided('Hint: add field \'id\' to the query schema')
        product = await StrawberryProductResolver.get_by_review_id(
            review_id=int(self.id), fields=required_fields,
        )
        return product

    @strawberry.field
    async def user(self, info: strawberry.Info) -> IUser:
        from src.users.graphql.resolver import StrawberryUserResolver
        required_fields = get_required_fields(info)
        if not self.id:
            raise IDIsNotProvided('Hint: add field \'id\' to the query schema')
        user = await StrawberryUserResolver.get_by_review_id(
            review_id=int(self.id), fields=required_fields,
        )
        return user


@strawberry.type
class DeletedReview(IDeleted):
    id: strawberry.ID
    success: bool
    message: str | None = None
