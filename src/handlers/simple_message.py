import datetime

from aiogram import types
from pycbrf import ExchangeRates

from loader import dp, bot
from ..services import (
    get_hello_message,
    get_dollar_message,
    get_pyjs_message
)


@dp.message_handler(text=get_hello_message())
async def welcome_message(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Привет {message.from_user.username}"
    )


@dp.message_handler(text=get_dollar_message())
async def get_dollar(message: types.Message):
    rates = ExchangeRates(
        str(datetime.datetime.now().date()), locale_en=True
    )
    current_usd = f'{rates["USD"].name} - {rates["USD"].value} руб.'
    await bot.send_message(
        chat_id=message.chat.id,
        text=current_usd
    )


@dp.message_handler(
    text=[
        "Леня ты кто?",
        "Леня ты кто",
        "леня ты кто?",
        "леня ты кто",
        "био",
        "bio"
    ]
)
async def get_bio(message: types.Message):
    text = """
    Привет, я детище одного НЕДОпрогера. Вот что я умею:
    1. Показывать курс доллара 💰. 
       Для этого напиши: доллар или Доллар;
        
    2. Пока все) 😘
    """
    await bot.send_message(
        chat_id=message.chat.id,
        text=text
    )


@dp.message_handler(text=get_pyjs_message())
async def get_pyjs(message: types.Message):
    with open("src/data/pyjs.jpg", "rb") as file:
        image = file.read()
    await bot.send_photo(message.chat.id, photo=image)


@dp.message_handler(text=["Максим", "максим", "Макс", "макс"])
async def hello(message: types.Message):
    sticker = "CAACAgIAAxkBAAEDoflh2CqUHby5Nfyui9G7kaP" \
              "E4AxfrwACHAIAAqzRchNIr_rSmKNEVyME"
    await bot.send_message(
        message.chat.id, text="@kozenkodev ХУЙЛО, ГОВНОКОДЕР!!!"
    )
    await bot.send_sticker(message.chat.id, sticker)
