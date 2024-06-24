import strawberry
from strawberry.types.nodes import Selection

from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.di import Container
from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.graphql import parse_id
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
        user_id: strawberry.ID | None = None,
        product_id: strawberry.ID | None = None,
    ) -> list[Review]:
        required_fields: list[str] = await cls._selections_to_strings(fields)
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            reviews = await uow.reviews.get_list(
                fields=required_fields,
                offset=offset,
                limit=limit,
                user_id=parse_id(user_id) if user_id is not None else user_id,
                product_id=parse_id(product_id) if product_id is not None else product_id,
            )
            await uow.commit()
        return [Review(**r.model_dump()) for r in reviews]

    @classmethod
    async def get(cls, id: strawberry.ID, fields: list[Selection]) -> Review | None:
        required_fields: list[str] = await cls._selections_to_strings(fields)
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            try:
                review = await uow.reviews.get(id=parse_id(id), fields=required_fields)
            except ObjectDoesNotExistException:
                return None
            await uow.commit()
        return Review(**review.model_dump())

    @classmethod
    async def create(cls, input: ReviewInput) -> Review:
        dto = ReviewDTO(**strawberry.asdict(input))
        dto.user_id = int(dto.user_id)
        dto.product_id = int(dto.product_id)
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            new_review: ReviewDTO = await uow.reviews.create(dto=dto)
        data = new_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    @classmethod
    async def update(cls, id: strawberry.ID, input: UpdateReviewInput) -> Review:
        dto = ReviewDTO(**strawberry.asdict(input))
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            updated_review: ReviewDTO = await uow.reviews.update(dto=dto, id=parse_id(id))
            await uow.commit()
        data = updated_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    @classmethod
    async def delete(cls, id: strawberry.ID) -> DeletedReview:
        uow = Container.resolve(AbstractReviewUnitOfWork)
        async with uow:
            is_deleted = await uow.reviews.delete(id=parse_id(id))
            await uow.commit()
        return DeletedReview(success=is_deleted, id=parse_id(id))
