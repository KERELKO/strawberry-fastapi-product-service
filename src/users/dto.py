from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int | None = None
    username: str = ''
