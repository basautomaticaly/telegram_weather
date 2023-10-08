from dataclasses import dataclass
from environs import Env


@dataclass
class DataBase:
    host: str
    port: int
    user: str
    password: str
    db_name: str


class ConfigProvider:
    def __init__(self, path=None):
        self.env = Env()
        self.env.read_env(path)

    def get_bot_token(self) -> str:
        return self.env('BOT_TOKEN')

    def get_chatGPT_key(self) -> str:
        return self.env('API_GPT')

    def get_weatherAPI_key(self) -> str:
        return self.env('API_KEY_WEATHER')

    def get_database_config(self):
        return DataBase(
            host=self.env('HOST'),
            port=self.env.int('PORT'),
            user=self.env('USER'),
            password=self.env('PASS'),
            db_name=self.env('DB_NAME')
        )
