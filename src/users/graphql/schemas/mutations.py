import strawberry

from src.common.base.graphql.schemas import IUser
from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.parsers import parse_id
from src.users.graphql.schemas.inputs import UpdateUserInput, UserInput
from src.users.graphql.schemas.queries import DeletedUser
from src.users.graphql.resolver import StrawberryUserResolver


@strawberry.type
class UserMutations:
    @strawberry.mutation
    async def register_user(self, input: UserInput) -> IUser:
        new_user = await StrawberryUserResolver.create(input=input)
        return new_user

    @strawberry.mutation
    async def update_user(self, id: strawberry.ID, input: UpdateUserInput) -> IUser:
        updated_user = await StrawberryUserResolver.update(input=input, id=parse_id(id))
        return updated_user

    @strawberry.mutation
    async def delete_user(self, id: strawberry.ID) -> DeletedUser:
        not_deleted = DeletedUser(id=id, success=False, message='User was not deleted')
        try:
            is_deleted = await StrawberryUserResolver.delete(id=parse_id(id))
        except ObjectDoesNotExistException:
            return not_deleted
        if is_deleted:
            return DeletedUser(id=id, success=True, message='User was deleted successfully!')
        return not_deleted
