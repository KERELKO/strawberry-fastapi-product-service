from src.common.base.dto import BaseDTO


class ReviewDTO(BaseDTO):
    content: str = ''


class CreateReviewDTO(BaseDTO):
    user_id: int
    product_id: int
    content: str


class ProductDTO(BaseDTO):
    title: str = ''
    description: str = ''
