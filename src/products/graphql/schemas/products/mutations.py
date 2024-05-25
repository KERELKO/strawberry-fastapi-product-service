import strawberry

from src.common.base.graphql.schemas import IProduct


@strawberry.type
class ProductMutations:
    @strawberry.mutation
    def add_product(self) -> IProduct:
        ...
