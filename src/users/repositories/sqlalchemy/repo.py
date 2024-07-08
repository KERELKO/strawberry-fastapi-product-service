import sqlalchemy as sql
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.common.db.sqlalchemy.extensions import _models_to_join, raise_exc, sqlalchemy_repo_extended
from src.common.db.sqlalchemy.models import Review, User
from src.common.db.sqlalchemy.base import BaseSQLAlchemyRepository
from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils.fields import SelectedFields
from src.products.dto import ReviewDTO
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserRepository


@sqlalchemy_repo_extended(query_executor=False)
class SQLAlchemyUserRepository(AbstractUserRepository, BaseSQLAlchemyRepository):
    class Meta:
        model = User

    def _construct_select_query(
        self,
        fields: list[SelectedFields],
        **queries,
    ) -> sql.Select:
        user_id = queries.get('id', None)
        offset = queries.get('offset', None)
        limit = queries.get('limit', None)
        _fields = fields[0].fields if len(fields) > 0 else raise_exc(Exception('No fields'))
        fields_to_select: list[InstrumentedAttribute] = [getattr(User, f) for f in _fields]
        stmt = sql.select(*fields_to_select)

        if user_id is not None:
            stmt = stmt.where(User.id == user_id)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        return stmt

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        list_values = await self._execute_query(fields=fields, offset=offset, limit=limit)
        dto_list = []
        for values in list_values:
            data = {field: value for field, value in zip(fields, values)}
            dto_list.append(UserDTO(**data))
        return dto_list

    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> UserDTO:
        values = await self._execute_query(
            fields=fields, review_id=review_id, first=True
        )
        if not values:
            raise ObjectDoesNotExistException('User')
        data = {}
        for value_index, field in enumerate(fields):
            data[field] = values[value_index]
        return UserDTO(**data)


class SQLAlchemyAggregatedUserRepository(SQLAlchemyUserRepository):
    async def _fetch_one_with_related(self, join_reviews: bool, **filters) -> User | None:
        user_id = filters.get('id', None)
        review_id = filters.get('review_id', None)
        stmt = sql.Select(User)
        if join_reviews:
            stmt = stmt.options(joinedload(User.reviews))
        if user_id is not None:
            stmt = stmt.where(User.id == user_id)
        elif review_id is not None:
            stmt = stmt.join(User.reviews)
            stmt = stmt.where(Review.id == review_id)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def _fetch_many_with_related(self, join_reviews: bool, **filters) -> list[User]:
        offset = filters.get('offset', 0)
        limit = filters.get('limit', 20)
        stmt = sql.Select(User).offset(offset).limit(limit)
        if join_reviews:
            stmt = stmt.options(joinedload(User.reviews))
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get(self, id: int, fields: list[SelectedFields]) -> UserDTO:
        _, _, join_review = _models_to_join(fields)
        _user = await self._fetch_one_with_related(id=id, join_reviews=join_review)
        if not _user:
            raise ObjectDoesNotExistException(User.__name__, id=id)
        user = UserDTO(**_user.as_dict())
        if join_review:
            reviews = [ReviewDTO(**r.as_dict()) for r in _user.reviews]
            user.reviews = reviews
        return user

    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> UserDTO:
        review: Review | None = await self.session.get(Review, id=review_id)
        if not review:
            raise ObjectDoesNotExistException('Review', object_id=review_id)
        return await self.get(id=review.user_id, fields=fields)

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        _, _, join_review = _models_to_join(fields)
        _users = await self._fetch_many_with_related(
            offset=offset, limit=limit, join_reviews=join_review,
        )
        users: list[UserDTO] = []
        for _user in _users:
            user = UserDTO(**_user.as_dict())
            if join_review:
                reviews = [ReviewDTO(**r.as_dict()) for r in _user.reviews]
                user.reviews = reviews
            users.append(user)
        return users
