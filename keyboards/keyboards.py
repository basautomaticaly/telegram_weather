from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class Keyboard:
    @staticmethod
    def build() -> ReplyKeyboardMarkup:
        # Инициализируем билдер
        kb_builder = ReplyKeyboardBuilder()
        # Создаем кнопки
        get_cloth_btn = KeyboardButton(text='Подобрать одежду')
        geo_btn = KeyboardButton(text='Отправить геолокацию', request_location=True)
        # Добавляем кнопки в билдер
        kb_builder.row(get_cloth_btn, geo_btn, width=1)
        # Создаем объект клавиатуры
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

