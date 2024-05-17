from sqlalchemy import select

from src.common.db.sqlalchemy.models import Review
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.products.dto import ReviewDTO
from src.products.repositories.base import AbstractReviewRepository


# TODO: remove hardcoding in repositories
class SQLAlchemyReviewRepository(AbstractReviewRepository, BaseSQLAlchemyRepository):
    async def get(self, id: int) -> ReviewDTO | None:
        stmt = select(Review).where(Review.id == id)
        result = self.session.execute(stmt)
        review = result.scalar().first()
        return ReviewDTO(
            id=id, text=review.text, user_id=review.user_id, product_id=review.product_id
        )

    async def get_list(self, *fields, offset: int = 0, limit: int = 20) -> list[ReviewDTO]:
        stmt = select(*[getattr(Review, f) for f in fields]).offset(offset).limit(limit)
        result = self.session.execute(stmt)
        reviews: list[ReviewDTO] = []
        for r in result.all():
            reviews.append(
                ReviewDTO(id=id, text=r.text, user_id=r.user_id, product_id=r.product_id)
            )
        return reviews
