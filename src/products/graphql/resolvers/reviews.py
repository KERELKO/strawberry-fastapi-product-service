import strawberry
from strawberry.types.nodes import Selection

from src.common.base.dto import ID
from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.di import Container
from src.common.exceptions import ObjectDoesNotExistException
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
        user_id: int | None = None,
        product_id: int | None = None,
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
    async def get(cls, id: ID, fields: list[Selection]) -> Review | None:
        required_fields: list[str] = await cls._get_list_fields(fields)
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            try:
                review = await uow.reviews.get(id=id, fields=required_fields)
            except ObjectDoesNotExistException:
                return None
            await uow.commit()
        return Review(**review.model_dump())

    @classmethod
    async def create(cls, input: ReviewInput) -> Review:
        dto = ReviewDTO(**strawberry.asdict(input))
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            new_review: ReviewDTO = await uow.reviews.create(dto=dto)
        data = new_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    @classmethod
    async def update(cls, id: ID, input: UpdateReviewInput) -> Review:
        dto = ReviewDTO(**strawberry.asdict(input))
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            updated_review: ReviewDTO = await uow.reviews.update(dto=dto, id=id)
            await uow.commit()
        data = updated_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    @classmethod
    async def delete(cls, id: ID) -> DeletedReview:
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            is_deleted = await uow.reviews.delete(id=id)
            await uow.commit()
        return DeletedReview(success=is_deleted, id=id)
