from motor.motor_asyncio import AsyncIOMotorClient

from src.common.settings import config


client = AsyncIOMotorClient(config.mongo_connection_string)
db = client.get_default_database()
