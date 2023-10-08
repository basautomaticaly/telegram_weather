import requests
import openai
from config_data.config import ConfigProvider

api_key = ConfigProvider()
openai.api_key = api_key.get_chatGPT_key()  # Используем await здесь

key = ConfigProvider()

async def get_info_weather(latitude: float, longitude: float) -> str:
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={key.get_weatherAPI_key()}'  # Используем await здесь
    print(url)
    resp = requests.get(url)  # Используем await здесь
    data = resp.json()  # Используем await здесь
    print(data)
    weather = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temp = data['main']['temp']
    feels_temp = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    quiz = f'Мне необходимо понимать что мне надеть, Я посмотрел сводку о погоде, не мог бы сказать, что мне надеть исходя из этих данных?' \
           f'обязательно назови полный комплект одежды и краткую сводку о погоде (температура, ветер, облачность)' \
           f'Погода {weather}' \
           f'Описание {description}' \
           f'Температура {temp}K' \
           f'Ощущается температура на {feels_temp}K' \
           f'Минимальная температура {temp_min}K' \
           f'Максимальная температура {temp_max}K' \
           f'Влажность {humidity}%' \
           f'Скорость ветра {wind_speed} метров в секунду'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=quiz,
        max_tokens=500,
        top_p=0.9,
        frequency_penalty=0.2,
        presence_penalty=0.2
    )
    return response.choices[0].text.strip()

