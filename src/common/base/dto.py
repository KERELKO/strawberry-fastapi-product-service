from enum import Enum

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(extra='allow')
    id: int | None = None


class Entity(str, Enum):
    USER: str = 'user'
    PRODUCT: str = 'product'
    REVIEW: str = 'review'
