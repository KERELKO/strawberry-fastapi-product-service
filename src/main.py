from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.graphql.schema import schema
from src.common.settings import config


def graphql_app() -> GraphQLRouter:
    graphql = GraphQLRouter(schema)
    return graphql


def fastapi_app() -> FastAPI:
    app = FastAPI(**config.app_config)
    app.include_router(graphql_app(), prefix='/graphql')
    return app
