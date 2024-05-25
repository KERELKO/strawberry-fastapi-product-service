from typing import Any, Type, TypeVar

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.common.base.uow import AbstractUnitOfWork
from src.common.exceptions import ObjectDoesNotExistException
from src.users.dto import UserDTO
from src.products.dto import ReviewDTO, ProductDTO

from .models import User, Product, Review
from .config import async_session_factory


MODELS_RELATED_TO_DTO = {
    User: UserDTO,
    Product: ProductDTO,
    Review: ReviewDTO,
}


SQLAlchemyModelType = TypeVar('SQLAlchemyModelType')
TypeDTO = TypeVar('TypeDTO')


class MetaSQLAlchemyRepository(type):
    """
    Add create, update and delete methods to subclass repository.
    All async.
    The subclass must implement Meta class inside with variable that contain SQLAlchemy model type
    """
    def __new__(
        cls,
        name: str,
        bases: tuple[Type[Any]],
        dct: dict[str, Any]
    ):
        def create_method(model: Type[SQLAlchemyModelType]):
            async def create(self, dto: TypeDTO, commit_after_creation: bool = True) -> TypeDTO:
                values = dto.model_dump()
                new_entity = model(**values)
                self.session.add(new_entity)
                if commit_after_creation:
                    await self.session.commit()
                    dto.id = new_entity.id
                return dto
            return create

        def update_method(model: Type[SQLAlchemyModelType]):
            async def update(self, id: int, dto: TypeDTO) -> TypeDTO:
                values: dict = dto.model_dump()
                if 'id' in values:
                    values.pop('id')
                stmt = (
                    sql.update(model)
                    .where(model.id == id)
                    .values(**values)
                    .returning(model)
                )
                result = await self.session.execute(stmt)
                updated_entity = result.scalar_one()
                if not updated_entity:
                    raise ObjectDoesNotExistException(model.__class__.__name__, object_id=id)
                dto_class = MODELS_RELATED_TO_DTO[model]
                return dto_class(**updated_entity.as_dict())
            return update

        def delete_method(model: Type[SQLAlchemyModelType]):
            async def delete(self, id: int) -> None:
                stmt = sql.select(model).where(model.id == id)
                result = await self.session.execute(stmt)
                entity = result.scalar_one()
                if not entity:
                    raise ObjectDoesNotExistException(model.__class__.__name__, object_id=id)
                await self.session.delete(entity)
                return True
            return delete

        if 'Meta' in dct:
            model = dct['Meta'].model
            dct['create'] = create_method(model)
            dct['update'] = update_method(model)
            dct['delete'] = delete_method(model)

        return super().__new__(cls, name, bases, dct)


class BaseSQLAlchemyRepository(metaclass=MetaSQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class BaseSQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker = async_session_factory) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()
