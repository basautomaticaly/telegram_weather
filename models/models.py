import pymysql
from pymysql import cursors
from config_data.config import ConfigProvider

class Database:
    _connection = None

    @classmethod
    async def connect_to_database(cls):
        if not cls._connection:
            database_config = ConfigProvider.get_database_config()
            cls._connection = await pymysql.connect(
                host=database_config.host,
                port=database_config.port,
                user=database_config.user,
                password=database_config.password,
                database=database_config.db_name,
                cursorclass=cursors.DictCursor
            )
        return cls._connection

    @classmethod
    async def disconnect_from_database(cls):
        if cls._connection:
            await cls._connection.close()