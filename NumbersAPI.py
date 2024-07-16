import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from googletrans import Translator
import requests

from config import TOKEN_TG05

# homework_TG05_bot
bot = Bot(token=TOKEN_TG05)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Введи число, а я сообщу интересный факт о нём")


@dp.message(Command('help'))
async def img_command_handler(message: Message):
    await message.answer("Этот бот сообщает интересный факт о введённом пользователем числе")


def translate_text_ru(en_text):
    translator = Translator()
    ru_text = translator.translate(en_text, src='en', dest='ru').text
    return ru_text


@dp.message()
async def get_number_fact(message: Message):
    number = message.text
    if number.isdigit():
        url = f'http://numbersapi.com/{number}'
        response = requests.get(url)
        if response.status_code == 200:
            number_info = translate_text_ru(response.text)
        else:
            number_info = f"Не удалось получить данные. Код ошибки: {response.status_code}"
    else:
        number_info = f"'{number}' не число. Попробуйте снова"
    await message.answer(number_info)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
