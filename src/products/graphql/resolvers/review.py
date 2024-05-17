from dataclasses import dataclass

from strawberry.utils.str_converters import to_snake_case
import strawberry

from src.products.graphql import schemas
from src.products.repositories.base import AbstractReviewUnitOfWork
from src.products.repositories.sqlalchemy.reviews.uow import SQLAlchemyReviewUnitOfWork


@dataclass
class StrawberryReviewResolver:
    unit_of_work: AbstractReviewUnitOfWork = SQLAlchemyReviewUnitOfWork

    async def get_list(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[schemas.Review]:
        fields: list[str] = []
        for selected_field in info.selected_fields:
            for field in selected_field.selections:
                fields.append(to_snake_case(field.name))

        uow = self.unit_of_work()
        async with uow:
            reviews = await uow.reviews.get_list(*fields, offset=offset, limit=limit)
            await uow.commit()
        return [schemas.Review(**r.model_dump()) for r in reviews]

    async def get(self, id: int) -> schemas.Review | None:
        uow = self.unit_of_work()
        async with uow:
            review = await uow.reviews.get(id=id)
            await uow.commit()
        if not review:
            return None
        return schemas.Review(**review.model_dump())
