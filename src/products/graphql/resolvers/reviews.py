from strawberry.types.nodes import Selection

from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.di import Container
from src.products.dto import ReviewDTO
from src.products.graphql.schemas.reviews.inputs import ReviewInput, UpdateReviewInput
from src.products.graphql.schemas.reviews.queries import DeletedReview, Review
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

    @classmethod
    async def create(cls, input: ReviewInput) -> Review:
        dto = ReviewDTO(**input.to_dict())
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            new_review: ReviewDTO = await uow.reviews.create(dto=dto)
        data = new_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    @classmethod
    async def update(cls, id: int, input: UpdateReviewInput) -> Review:
        dto = ReviewDTO(**input.to_dict())
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            updated_review: ReviewDTO = await uow.reviews.update(dto=dto, id=id)
            await uow.commit()
        data = updated_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    @classmethod
    async def delete(cls, id: int) -> DeletedReview:
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            is_deleted = await uow.reviews.delete(id=id)
            await uow.commit()
        return DeletedReview(success=is_deleted, id=id)
