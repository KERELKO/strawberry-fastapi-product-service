from pydantic import BaseModel, ConfigDict


class ReviewDTO(BaseModel):
    model_config = ConfigDict(extra='allow')
    id: int | None = None
    content: str = ''


class ProductDTO(BaseModel):
    id: int | None = None
    title: str = ''
    description: str = ''
