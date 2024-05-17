from pydantic import BaseModel


class ReviewDTO(BaseModel):
    id: int | None = None
    # user_id: int | None = None
    text: str = ''


class ProductDTO(BaseModel):
    id: int | None = None
    title: str = ''
    description: str = ''
    # reviews: list[ReviewDTO] = Field(default_factory=list)
