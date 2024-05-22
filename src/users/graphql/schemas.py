import strawberry
import strawberry.mutation

from src.common.base.graphql.schemas import IUser
from src.common.utils.graphql import get_required_fields
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.schemas.reviews import Review


@strawberry.type
class User(IUser):
    id: strawberry.ID
    username: str

    @strawberry.field
    def reviews(self, info: strawberry.Info, offset: int = 0, limit: int = 20) -> list[Review]:
        if not self.id:
            return []
        fields = get_required_fields(info)
        reviews = StrawberryReviewResolver.get_list(
            fields=fields, user_id=self.id, offset=offset, limit=limit,
        )
        return reviews


@strawberry.input
class UserInput:
    username: str


@strawberry.input
class UpdateUserInput:
    username: str


@strawberry.type
class DeletedUser:
    success: bool
    id: strawberry.ID
    message: str | None = None


@strawberry.type
class UserMutations:
    @strawberry.mutation
    def add_user(self, input: UserInput) -> IUser:
        return User(id="1", username=input.username)

    @strawberry.mutation
    def update_user(self, input: UpdateUserInput) -> IUser:
        return User(id="1", username=input.username)

    @strawberry.mutation
    def delete_user(self, id: strawberry.ID) -> DeletedUser:
        return DeletedUser(id=id, success=True, message='User was deleted successfully!')
