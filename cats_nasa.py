import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from datetime import datetime, timedelta
import requests
import random

from config import TOKEN, THE_CAT_API_KEY, NASA_API_KEY

# lesson_TG05_bot
bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']


def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None


def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}"
    response = requests.get(url)
    return response.json()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Введи команды: /cat или /apod")


@dp.message(Command("cat"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши мне название породы кошки, и я пришлю тебе её фото и описание")


@dp.message(Command("apod"))
async def random_apod(message: Message):
    apod = get_random_apod()
    title = apod['title']
    photo_url = apod['url']
    await message.answer_photo(photo=photo_url, caption=f"{title}")


@dp.message()
async def send_cat_info(message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info:
        cat_image_url = get_cat_image_by_breed(breed_info['id'])
        info = (
            f"Порода: {breed_info['name']}\n"
            f"Описание: {breed_info['description']}\n"
            f"Продолжительность жизни: {breed_info['life_span']} лет"
        )
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        await message.answer("Порода не найдена. Попробуйте еще раз.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
