from dataclasses import dataclass

import strawberry
from strawberry.types.nodes import Selection

from src.common.base.graphql.resolvers import BaseStrawberryResolver
from src.common.utils.fields import SelectedFields
from src.common.utils.graphql import parse_id
from src.products.dto import ReviewDTO, CreateReviewDTO
from src.products.graphql.schemas.reviews.inputs import ReviewInput, UpdateReviewInput
from src.products.graphql.schemas.reviews.queries import DeletedReview, Review
from src.products.graphql.converters.reviews import StrawberryReviewConverter
from src.products.services.reviews import ReviewService


@dataclass(eq=False, repr=False)
class StrawberryReviewResolver(BaseStrawberryResolver):
    service: ReviewService

    async def get_list(
        self,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
        user_id: strawberry.ID | None = None,
        product_id: strawberry.ID | None = None,
    ) -> list[Review]:
        required_fields: list[SelectedFields] = self._selections_to_selected_fields(
            fields, remove_related=False,
        )
        reviews = await self.service.get_review_list(
            fields=required_fields,
            offset=offset,
            limit=limit,
            user_id=parse_id(user_id) if user_id else None,
            product_id=parse_id(product_id) if product_id else None,
        )
        return [StrawberryReviewConverter.convert(r) for r in reviews]

    async def get(self, id: strawberry.ID, fields: list[Selection]) -> Review | None:
        required_fields: list[SelectedFields] = self._selections_to_selected_fields(
            fields, remove_related=False,
        )
        review = await self.service.get_review_by_id(fields=required_fields, id=parse_id(id))
        return StrawberryReviewConverter.convert(review) if review else None

    async def create(self, input: ReviewInput) -> Review:
        data = strawberry.asdict(input)
        data['user_id'] = int(data['user_id'])
        data['product_id'] = int(data['product_id'])

        dto = CreateReviewDTO(**data)
        new_review = await self.service.create_review(dto=dto)

        data = new_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')

        return Review(**data)

    async def update(self, id: strawberry.ID, input: UpdateReviewInput) -> Review | None:
        dto = ReviewDTO(**strawberry.asdict(input))
        review = await self.service.update_review(id=parse_id(id), dto=dto)
        if not review:
            return None
        data = review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    async def delete(self, id: strawberry.ID) -> DeletedReview:
        is_deleted = await self.service.delete_review(id=parse_id(id))
        return DeletedReview(success=is_deleted, id=id)
