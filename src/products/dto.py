from pydantic import BaseModel


class ReviewDTO(BaseModel):
    id: int | None = None
    content: str = ''
    product_id: int | None = None


class ProductDTO(BaseModel):
    id: int | None = None
    title: str = ''
    description: str = ''
