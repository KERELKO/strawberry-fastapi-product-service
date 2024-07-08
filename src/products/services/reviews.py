from dataclasses import dataclass

from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.fields import SelectedFields
from src.products.dto import ReviewDTO
from src.products.repositories.base import AbstractReviewUnitOfWork


@dataclass(eq=False, repr=False)
class ReviewService:
    uow: AbstractReviewUnitOfWork

    async def get_review_by_id(self, id: int, fields: list[SelectedFields]) -> ReviewDTO | None:
        async with self.uow:
            try:
                review = await self.uow.reviews.get(id=id, fields=fields)
            except ObjectDoesNotExistException:
                return None
        return review

    async def get_review_list(
        self,
        fields: list[SelectedFields],
        offset: int,
        limit: int,
        user_id: int | None = None,
        product_id: int | None = None,
    ) -> list[ReviewDTO]:
        async with self.uow:
            reviews = await self.uow.reviews.get_list(
                fields=fields,
                offset=offset,
                limit=limit,
                user_id=user_id,
                product_id=product_id,
            )
        return reviews

    async def create_review(self, dto: ReviewDTO) -> ReviewDTO:
        async with self.uow:
            new_review: ReviewDTO = await self.uow.reviews.create(dto=dto)
            self.uow.commit()
        return new_review

    async def update_review(self, id: int, dto: ReviewDTO) -> ReviewDTO | None:
        async with self.uow:
            try:
                updated_review: ReviewDTO = await self.uow.reviews.update(dto=dto, id=id)
            except ObjectDoesNotExistException:
                return None
            await self.uow.commit()
        return updated_review

    async def delete_review(self, id: int) -> bool:
        async with self.uow:
            is_deleted = await self.uow.reviews.delete(id=id)
            await self.uow.commit()
        return is_deleted
