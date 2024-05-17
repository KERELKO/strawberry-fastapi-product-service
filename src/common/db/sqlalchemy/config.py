from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.common.settings import config


engine = create_async_engine(config.postgres_connection_string)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=True
)
