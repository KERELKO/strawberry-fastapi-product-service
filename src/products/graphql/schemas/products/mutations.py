import strawberry

from src.common.base.graphql.schemas import IProduct
from src.common.exceptions import ObjectDoesNotExistException
from src.products.graphql.resolvers.products import StrawberryProductResolver
from src.products.graphql.schemas.products.inputs import ProductInput, UpdateProductInput
from src.products.graphql.schemas.products.queries import DeletedProduct


@strawberry.type
class ProductMutations:
    @strawberry.mutation
    async def create_product(self, input: ProductInput) -> IProduct:
        new_product = await StrawberryProductResolver.create(input=input)
        return new_product

    @strawberry.mutation
    async def update_product(self, id: strawberry.ID, input: UpdateProductInput) -> IProduct:
        updated_product = await StrawberryProductResolver.update(input=input, id=int(id))
        return updated_product

    @strawberry.mutation
    async def delete_product(self, id: strawberry.ID) -> DeletedProduct:
        try:
            deleted = await StrawberryProductResolver.delete(id=int(id))
        except ObjectDoesNotExistException:
            deleted.message = 'Product with given ID is not found'
            return deleted
        return deleted
