import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from googletrans import Translator
import requests

from config import TOKEN_TG05, UNSPLASH_ACCESS_KEY

# Access Key для Unsplash API
access_key = UNSPLASH_ACCESS_KEY

bot = Bot(token=TOKEN_TG05)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Введите текстовый запрос для поиска изображений:")


@dp.message(Command('help'))
async def img_command_handler(message: Message):
    await message.answer("Этот бот выводит три изображения по текстовому запросу на русском или английском языках")


# Ищем 3 картинки по запросу
def get_image_urls(query, per_page=3):
    url = 'https://api.unsplash.com/search/photos'
    headers = {'Authorization': f'Client-ID {access_key}'}
    params = {
        'query': query,
        'per_page': per_page
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        image_urls = [result['urls']['regular'] for result in data['results']]
        return image_urls
    else:
        print(f'Ошибка: {response.status_code}')
        return []


def translate_text_en(ru_text):
    translator = Translator()
    en_text = translator.translate(ru_text, src='ru', dest='en').text
    return en_text


# Хэндлер для получения текстового запроса
@dp.message(F.text)
async def text_message_handler(message: Message):
    query = translate_text_en(message.text)
    image_urls = get_image_urls(query)

    if image_urls:
        for url in image_urls:
            await message.answer_photo(url)
    else:
        await message.answer("Не удалось найти изображения по вашему запросу.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
