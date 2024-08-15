from fastapi import FastAPI

import strawberry
from strawberry.fastapi import GraphQLRouter

from src.common.graphql.query import Query
from src.common.graphql.mutations import Mutation
from src.common.settings import config


def graphql_app() -> GraphQLRouter:
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql: GraphQLRouter = GraphQLRouter(schema)

    return graphql


def fastapi_app() -> FastAPI:
    app = FastAPI(**config.app_config)
    app.include_router(graphql_app(), prefix='/graphql')

    return app
