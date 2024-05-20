from fastapi import FastAPI

from strawberry.fastapi import GraphQLRouter

from src.common.db.sqlalchemy.config import engine
from src.common.db.sqlalchemy.models import Base
from src.common.graphql_schema import schema
from src.common.middlewares import ExecutingTimeMiddleware
from src.common.settings import config


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def graphql_app() -> GraphQLRouter:
    graphql = GraphQLRouter(schema)
    return graphql


def fastapi_app() -> FastAPI:
    app = FastAPI(**config.app_config)
    app.include_router(graphql_app(), prefix='/graphql')

    # Middlewares
    app.add_middleware(ExecutingTimeMiddleware)

    return app
