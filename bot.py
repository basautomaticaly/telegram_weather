import asyncio
from handlers import user_handlers
from config_data.config import ConfigProvider
from models.models import Database
from aiogram import Bot, Dispatcher
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import pymysql


# функция конфигурирования и запуска бота
async def main():
    # загрузка конфига в переменную config
    config_provider = ConfigProvider()
    token_bot: str = config_provider.get_bot_token()
    # Инициализация бота и диспетчера
    bot = Bot(token=token_bot)
    dp = Dispatcher()
    #подключаемся к бд
    dp.include_router(user_handlers.router)
    #делаем что-то

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)




dp = Dispatcher()
bot = Bot(token='6423820458:AAElOMfj6e6K4UiEWSLmp2qboMGUpVQefsw')

import requests

# Параметры запроса
api_key = '1223c16760b94b55916113405230710'

# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()

# Создаем кнопки
contact_btn = KeyboardButton(
    text='Отправить телефон',
    request_contact=True
)
geo_btn = KeyboardButton(
    text='Отправить геолокацию',
    request_location=True
)
poll_btn = KeyboardButton(
    text='Создать опрос/викторину',
    request_poll=KeyboardButtonPollType()
)

# Добавляем кнопки в билдер
kb_builder.row(contact_btn, geo_btn, poll_btn, width=1)

# Создаем объект клавиатуры
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)







if __name__ == '__main__':
    asyncio.run(main())
