from functools import cache
from typing import Type, TypeVar
import logging

import punq

from src.common.db.mongo.base import FakeMongoUnitOfWork
from src.products.repositories.base import (
    IProductRepository,
    AbstractProductUnitOfWork,
    IReviewRepository,
    AbstractReviewUnitOfWork,
)
from src.products.repositories.sqlalchemy.products.repo import SQLAlchemyProductRepository
from src.products.repositories.sqlalchemy.products.uow import SQLAlchemyProductUnitOfWork
from src.products.repositories.sqlalchemy.reviews.repo import SQLAlchemyReviewRepository
from src.products.repositories.sqlalchemy.reviews.uow import SQLAlchemyReviewUnitOfWork
from src.users.repositories.base import IUserRepository, AbstractUserUnitOfWork
from src.users.repositories.mongo.repo import MongoUserRepository
# from src.users.repositories.sqlalchemy.repo import SQLAlchemyUserRepository
# from src.users.repositories.sqlalchemy.uow import SQLAlchemyUserUnitOfWork


T = TypeVar('T')


class Container:
    @cache
    @staticmethod
    def get() -> punq.Container:
        return Container._init()

    @staticmethod
    def resolve(base_cls: Type[T]) -> T:
        return Container.get().resolve(base_cls)

    @staticmethod
    def _init() -> punq.Container:
        container = punq.Container()

        logger = logging.getLogger('Logger')
        container.register(logging.Logger, instance=logger)

        container.register(IUserRepository, MongoUserRepository)
        container.register(AbstractUserUnitOfWork, FakeMongoUnitOfWork)

        container.register(IReviewRepository, SQLAlchemyReviewRepository)
        container.register(AbstractReviewUnitOfWork, SQLAlchemyReviewUnitOfWork)

        container.register(IProductRepository, SQLAlchemyProductRepository)
        container.register(AbstractProductUnitOfWork, SQLAlchemyProductUnitOfWork)

        return container
