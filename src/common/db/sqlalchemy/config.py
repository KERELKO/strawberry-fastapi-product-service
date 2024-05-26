from logging import Logger

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import event

from src.common.settings import config


engine = create_async_engine(config.postgres_connection_string)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

if config.LISTEN_SQL_QUERIES:
    @event.listens_for(engine.sync_engine, 'before_execute')
    def sql_statement_listener(conn, clauseelement, multiparams, params):
        from src.common.di import Container

        logger = Container.resolve(Logger)
        if config.DEBUG:
            print(f'{'SQL stmt':-^40}\n{clauseelement}\n{'':-^40}')
        logger.info(f'SQL stmt: {clauseelement}')
