from abc import abstractmethod
from typing import Any, Callable, Type, TypeVar

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.common.base.dto import BaseDTO
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

SQLAlchemyModel = TypeVar('SQLAlchemyModel', bound=User | Product | Review)
TypeDTO = TypeVar('TypeDTO', bound=BaseDTO)


class MetaSQLAlchemyRepository(type):
    """
    Add create, update and delete methods to subclass repository.
    All async.
    The subclass must implement Meta class inside with variable that contains SQLAlchemy model type
    """
    def __new__(
        cls,
        name: str,
        bases: tuple[Type[Any], ...],
        cls_attrs: dict[str, Any]
    ) -> 'MetaSQLAlchemyRepository':
        def create_method(model: Type[SQLAlchemyModel]) -> Callable:
            async def create(self, dto: TypeDTO, commit_after_creation: bool = True) -> TypeDTO:
                values = dto.model_dump()
                new_entity = model(**values)
                self.session.add(new_entity)
                if commit_after_creation:
                    await self.session.commit()
                    dto.id = new_entity.id
                return dto
            return create

        def update_method(model: Type[SQLAlchemyModel]) -> Callable:
            async def update(self, id: int, dto: TypeDTO) -> TypeDTO:
                values: dict = dto.model_dump()
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
                    raise ObjectDoesNotExistException(model.__name__, object_id=id)
                dto_class = MODELS_RELATED_TO_DTO[model]
                return dto_class(**updated_entity.as_dict())
            return update

        def delete_method(model: Type[SQLAlchemyModel]) -> Callable:
            async def delete(self, id: int) -> bool:
                stmt = sql.select(model).where(model.id == id)
                result = await self.session.execute(stmt)
                entity = result.scalar_one()
                if not entity:
                    raise ObjectDoesNotExistException(model.__name__, object_id=id)
                await self.session.delete(entity)
                return True
            return delete

        if 'Meta' in cls_attrs:
            model = cls_attrs['Meta'].model
            cls_attrs['create'] = create_method(model)
            cls_attrs['update'] = update_method(model)
            cls_attrs['delete'] = delete_method(model)

        return super().__new__(cls, name, bases, cls_attrs)


class BaseSQLAlchemyRepository(metaclass=MetaSQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    async def _construct_select_query(self, *args, **queries) -> sql.Select:
        """
        Implement the method to make "_execute_query" work,
        params can be overriden with specific ones
        """

    async def _execute_query(
        self,
        *args,
        first: bool = False,
        **kwargs,
    ) -> list[tuple[Any]] | tuple[Any]:
        stmt = await self._construct_select_query(*args, **kwargs)
        result = await self.session.execute(stmt)
        if first:
            return result.first()  # type: ignore
        return result.all()  # type: ignore


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
