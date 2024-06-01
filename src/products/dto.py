from src.common.base.dto import BaseDTO


class ReviewDTO(BaseDTO):
    content: str = ''


class ProductDTO(BaseDTO):
    title: str = ''
    description: str = ''
