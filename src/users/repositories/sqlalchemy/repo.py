from sqlalchemy import select

from src.common.db.sqlalchemy.models import User
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.users.repositories.base import AbstractUserRepository
from src.users.dto import UserDTO


class SQLAlchemyUserRepository(AbstractUserRepository, BaseSQLAlchemyRepository):
    async def get_list(
        self,
        *fields: tuple[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        stmt = select(*[getattr(User, f) for f in fields]).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        users: list[tuple[User]] = result.all()
        return [UserDTO(id=u.id, first_name=u.first_name, last_name=u.last_name) for u in users]

    async def get(self, id: int) -> UserDTO | None:
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None
        return UserDTO(id=user.id, first_name=user.first_name, last_name=user.last_name)
