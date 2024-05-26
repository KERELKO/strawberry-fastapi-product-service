from pydantic import ConfigDict

from src.common.base.dto import BaseDTO


class ReviewDTO(BaseDTO):
    model_config = ConfigDict(extra='allow')
    content: str = ''


class ProductDTO(BaseDTO):
    title: str = ''
    description: str = ''
