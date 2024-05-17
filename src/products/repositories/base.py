from src.products.dto import ProductDTO, ReviewDTO
from src.common.repo import AbstractRepository
from src.common.uow import AbstractUnitOfWork


# TODO: type hints
class AbstractProductRepository[ProductDTO](AbstractRepository):
    ...


class AbstractReviewRepository[ReviewDTO](AbstractRepository):
    ...


class AbstractProductUnitOfWork(AbstractUnitOfWork):
    products: AbstractProductRepository


class AbstractReviewUnitOfWork(AbstractUnitOfWork):
    reviews: AbstractReviewRepository
