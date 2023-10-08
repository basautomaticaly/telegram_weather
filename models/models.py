import aiomysql
from aiomysql import cursors
from config_data.config import ConfigProvider

class Database:
    _pool = None

    @classmethod
    async def create_pool(cls):
        if not cls._pool:
            database_config = ConfigProvider().get_database_config()  # Note: Added () to create an instance
            cls._pool = await aiomysql.create_pool(
                host=database_config.host,
                port=database_config.port,
                user=database_config.user,
                password=database_config.password,
                db=database_config.db_name,
                cursorclass=cursors.DictCursor,
                autocommit=True
            )

    @classmethod
    async def connect_to_database(cls):
        await cls.create_pool()
        return cls._pool

    @classmethod
    async def disconnect_from_database(cls):
        if cls._pool:
            cls._pool.close()
            await cls._pool.wait_closed()