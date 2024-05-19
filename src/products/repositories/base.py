from src.products.dto import ProductDTO, ReviewDTO
from src.common.base.repo import AbstractRepository
from src.common.base.uow import AbstractUnitOfWork


class AbstractProductRepository(AbstractRepository[ProductDTO]):
    ...


class AbstractReviewRepository(AbstractRepository[ReviewDTO]):
    ...


class AbstractProductUnitOfWork(AbstractUnitOfWork):
    products: AbstractProductRepository


class AbstractReviewUnitOfWork(AbstractUnitOfWork):
    reviews: AbstractReviewRepository
