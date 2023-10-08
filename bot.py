import asyncio
from models import models, methods
from config_data.config import ConfigProvider
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import pymysql


# функция конфигурирования и запуска бота
async def main():
    # загрузка конфига в переменную config
    token_bot: str = ConfigProvider.get_bot_token()
    # Инициализация бота и диспетчера
    bot = Bot(token=token_bot)
    dp = Dispatcher()
    #подключаемся к бд
    connection = await models.connect_to_database()
    print('Connected to the database')
    #делаем что-то




try:
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='mysql',
        password='mysql',
        database='tele_weather',
        cursorclass=pymysql.cursors.DictCursor
    )
    print('good')
    try:
        with connection.cursor() as cursor:
            select_alls = "INSERT INTO `user` (user_id, latitude, longitude) VALUES ('213','22.3','11.2');"
            cursor.execute(select_alls)
            connection.commit()
        with connection.cursor() as cursor:
            select_all = "SELECT * FROM `user`"
            cursor.execute(select_all)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    finally:
        connection.close()
except Exception as ex:
    print(f'Failed {ex}')

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


@dp.message(F.content_type == ContentType.LOCATION)
async def process_start_command(message: Message):
    print(message)
    latitude = message.location.latitude
    longitude = message.location.longitude
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}'
    response = requests.get(url)

    # Проверка статуса ответа
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f'Error: {response.status_code}')
    await message.answer(
        text=f'{data}Спасибо за вашу геолокацию',
        reply_markup=keyboard
    )


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Экспериментируем со специальными кнопками',
        reply_markup=keyboard
    )


if __name__ == '__main__':
    asyncio.run(main())
