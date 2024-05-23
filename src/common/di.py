from functools import cache
from typing import Type, TypeVar
import logging

import punq

from src.products.repositories.base import (
    AbstractProductRepository,
    AbstractProductUnitOfWork,
    AbstractReviewRepository,
    AbstractReviewUnitOfWork,
)
from src.products.repositories.sqlalchemy.products.repo import SQLAlchemyProductRepository
from src.products.repositories.sqlalchemy.products.uow import SQLAlchemyProductUnitOfWork
from src.products.repositories.sqlalchemy.reviews.repo import SQLAlchemyReviewRepository
from src.products.repositories.sqlalchemy.reviews.uow import SQLAlchemyReviewUnitOfWork
from src.users.repositories.base import AbstractUserRepository, AbstractUserUnitOfWork
from src.users.repositories.sqlalchemy.repo import SQLAlchemyUserRepository
from src.users.repositories.sqlalchemy.uow import SQLAlchemyUserUnitOfWork


T = TypeVar('T')


class Container:
    @cache
    @staticmethod
    def get() -> punq.Container:
        return Container._init()

    @staticmethod
    def resolve(cls: Type[T]) -> T:
        return Container.get().resolve(cls)

    @staticmethod
    def _init() -> punq.Container:
        container = punq.Container()

        logger = logging.getLogger('Logger')
        container.register(logging.Logger, instance=logger)

        container.register(AbstractUserRepository, SQLAlchemyUserRepository)
        container.register(AbstractUserUnitOfWork, SQLAlchemyUserUnitOfWork)

        container.register(AbstractReviewRepository, SQLAlchemyReviewRepository)
        container.register(AbstractReviewUnitOfWork, SQLAlchemyReviewUnitOfWork)

        container.register(AbstractProductRepository, SQLAlchemyProductRepository)
        container.register(AbstractProductUnitOfWork, SQLAlchemyProductUnitOfWork)

        return container
