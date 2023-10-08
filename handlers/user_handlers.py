from aiogram import F
from aiogram.types import Message, ContentType
from aiogram.filters import CommandStart, Command
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import Keyboard
from aiogram import Router
from models import methods
from models.models import Database
from services.services import get_info_weather

router = Router()
keyboard_markup = Keyboard.build()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=keyboard_markup)


@router.message(Command(commands='/help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(F.content_type == ContentType.LOCATION)
async def process_geo_command(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    pool = await Database.connect_to_database()
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            if await methods.check_user_exists(connection=connection, user_id=message.from_user.id):
                await methods.update_user_location(connection=connection,
                                                   user_id=message.from_user.id,
                                                   latitude=latitude,
                                                   longitude=longitude
                                                   )
            else:
                await methods.insert_user(connection=connection,
                                          user_id=message.from_user.id,
                                          latitude=latitude,
                                          longitude=longitude
                                          )
    await message.answer(text=LEXICON_RU['Get_geo'], reply_markup=keyboard_markup)


@router.message(F.text == 'Подобрать одежду')
async def process_cloth_message(message: Message):
    pool = await Database.connect_to_database()
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            if await methods.check_user_exists(connection=connection, user_id=message.from_user.id):
                coords = await methods.get_user_coords(connection=connection, user_id=message.from_user.id)
                await message.answer(text=f'Ваши координаты: широта {coords["latitude"]} и долгота {coords["longitude"]}', reply_markup=keyboard_markup)
                answer = await get_info_weather(latitude=coords["latitude"],longitude=coords["longitude"])
                await message.answer(
                    text=answer,
                    reply_markup=keyboard_markup)
            else:
                await message.answer(text=LEXICON_RU['None'], reply_markup=keyboard_markup)


