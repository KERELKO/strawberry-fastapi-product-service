from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int | None = None
    first_name: str = ''
    last_name: str = ''
