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
    _product: IProduct | None = strawberry.field(
        default=None,
        name='_product',
        description='Do not use this field for queries, use "product" instead',
    )
    _user: IUser | None = strawberry.field(
        default=None,
        name='_user',
        description='Do not use this field for queries, use "user" instead',
    )

    @strawberry.field
    async def product(self, info: strawberry.Info) -> IProduct | None:
        from src.products.graphql.resolvers.products import StrawberryProductResolver
        required_fields = get_required_fields(info)
        if self._product is not None:
            return self._product
        if self._product_id:
            product = await StrawberryProductResolver.get(
                id=int(self._product_id), fields=required_fields,
            )
        else:
            if not self.id:
                raise IDIsNotProvided('Hint: add field \'id\' to the query schema')
            product = await StrawberryProductResolver.get_by_review_id(
                review_id=int(self.id), fields=required_fields,
            )
        return product

    @strawberry.field
    async def user(self, info: strawberry.Info) -> IUser | None:
        from src.users.graphql.resolver import StrawberryUserResolver
        required_fields = get_required_fields(info)
        if self._user is not None:
            return self._user
        if not self.id:
            raise IDIsNotProvided('Hint: add field \'id\' to the query schema')
        if self._user_id:
            user = await StrawberryUserResolver.get(
                id=int(self._user_id), fields=required_fields,
            )
        else:
            user = await StrawberryUserResolver.get_by_review_id(
                review_id=int(self.id), fields=required_fields,
            )
        return user


@strawberry.type
class DeletedReview(IDeleted):
    id: strawberry.ID
    success: bool
    message: str | None = None
