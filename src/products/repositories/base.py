from abc import abstractmethod
from src.common.base.dto import ID
from src.products.dto import ProductDTO, ReviewDTO
from src.common.base.repo import AbstractRepository
from src.common.base.uow import AbstractUnitOfWork


class AbstractProductRepository(AbstractRepository[ProductDTO]):
    @abstractmethod
    async def get_by_review_id(self, review_id: ID, fields: list[str]) -> ProductDTO:
        ...


class AbstractReviewRepository(AbstractRepository[ReviewDTO]):
    @abstractmethod
    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
        product_id: ID | None = None,
        user_id: ID | None = None,
    ) -> list[ReviewDTO]:
        ...


class AbstractProductUnitOfWork(AbstractUnitOfWork):
    products: AbstractProductRepository


class AbstractReviewUnitOfWork(AbstractUnitOfWork):
    reviews: AbstractReviewRepository
