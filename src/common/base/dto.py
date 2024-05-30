from pydantic import BaseModel


class BaseDTO(BaseModel):
    id: int | None = None
