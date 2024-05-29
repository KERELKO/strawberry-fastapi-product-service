from typing import Union

from pydantic import BaseModel


ID = Union[str, int]


class BaseDTO(BaseModel):
    id: ID | None = None
