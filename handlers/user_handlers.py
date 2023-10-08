from aiogram import F
from aiogram.types import Message, ContentType
from aiogram.filters import CommandStart, Command
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import Keyboard
from aiogram import Router
from models import methods
from models.models import Database

router = Router()
keyboard = Keyboard()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=keyboard)


@router.message(Command(commands='/help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

@router.message(F.content_type == ContentType.LOCATION)
async def process_start_command(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    connection = await Database.connect_to_database()

    if methods.check_user_exists(message.from_user.id):
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
    await message.answer(
        text=f'{data}Спасибо за вашу геолокацию',
        reply_markup=keyboard
    )
    await Database.disconnect_from_database()

@router.message(F.text == 'Подобрать одежду')
async def process_cloth_message(message: Message):
    connection = await Database.connect_to_database()
    if methods.check_user_exists(connection=connection, user_id=message.from_user.id):
        pass
    else:
        await message.answer(text=LEXICON_RU['None'], reply_markup=keyboard)
    await Database.disconnect_from_database()



@router.message(F.content_type == ContentType.LOCATION)
async def process_start_command(message: Message):
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
