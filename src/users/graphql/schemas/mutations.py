import strawberry

from src.common.base.graphql.schemas import IUser
from src.common.exceptions import ObjectDoesNotExistException
from src.users.graphql.schemas.inputs import UpdateUserInput, UserInput
from src.users.graphql.schemas.queries import DeletedUser
from src.users.graphql.resolver import StrawberryUserResolver
from src.common.di import Container


@strawberry.type
class UserMutations:
    @strawberry.mutation
    async def register_user(self, input: UserInput) -> IUser:
        resolver: StrawberryUserResolver = Container.resolve(StrawberryUserResolver)
        new_user = await resolver.create(input=input)
        return new_user

    @strawberry.mutation
    async def update_user(self, id: strawberry.ID, input: UpdateUserInput) -> IUser | None:
        resolver: StrawberryUserResolver = Container.resolve(StrawberryUserResolver)
        updated_user = await resolver.update(input=input, id=id)
        return updated_user

    @strawberry.mutation
    async def delete_user(self, id: strawberry.ID) -> DeletedUser:
        resolver: StrawberryUserResolver = Container.resolve(StrawberryUserResolver)
        not_deleted = DeletedUser(id=id, success=False, message='User was not deleted')
        try:
            is_deleted = await resolver.delete(id=id)
        except ObjectDoesNotExistException:
            return not_deleted
        if is_deleted:
            return DeletedUser(id=id, success=True, message='User was deleted successfully!')
        return not_deleted
