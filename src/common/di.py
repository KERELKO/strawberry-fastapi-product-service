from functools import cache
from typing import Any, Type

import punq

from src.products.repositories.base import AbstractReviewRepository, AbstractReviewUnitOfWork
from src.products.repositories.sqlalchemy.reviews.repo import SQLAlchemyReviewRepository
from src.products.repositories.sqlalchemy.reviews.uow import SQLAlchemyReviewUnitOfWork
from src.users.repositories.base import AbstractUserRepository, AbstractUserUnitOfWork
from src.users.repositories.sqlalchemy.repo import SQLAlchemyUserRepository
from src.users.repositories.sqlalchemy.uow import SQLAlchemyUserUnitOfWork


class Container:
    @cache
    @staticmethod
    def get() -> punq.Container:
        return Container._init()

    @staticmethod
    def resolve(cls: Type[Any]) -> Any:
        return Container.get().resolve(cls)

    @staticmethod
    def _init() -> punq.Container:
        container = punq.Container()

        container.register(AbstractUserRepository, SQLAlchemyUserRepository)
        container.register(AbstractUserUnitOfWork, SQLAlchemyUserUnitOfWork)

        container.register(AbstractReviewRepository, SQLAlchemyReviewRepository)
        container.register(AbstractReviewUnitOfWork, SQLAlchemyReviewUnitOfWork)
        return container
