from strawberry.types.nodes import Selection

from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.di import Container
from src.products.graphql.schemas.reviews import Review
from src.products.repositories.base import AbstractReviewUnitOfWork


class StrawberryReviewResolver(BaseStrawberryResolver):
    @classmethod
    async def get_list(
        cls,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
        user_id: int = None,
        product_id: int = None,
    ) -> list[Review]:
        required_fields: list[str] = await cls._get_list_fields(fields)
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            reviews = await uow.reviews.get_list(
                fields=required_fields,
                offset=offset,
                limit=limit,
                user_id=user_id,
                product_id=product_id,
            )
            await uow.commit()
        return [Review(**r.model_dump()) for r in reviews]

    @classmethod
    async def get(cls, id: int, fields: list[Selection]) -> Review | None:
        required_fields: list[str] = await cls._get_list_fields(fields)
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            review = await uow.reviews.get(id=id, fields=required_fields)
            await uow.commit()
        if not review:
            return None
        return Review(**review.model_dump())
