import datetime
import random

from aiogram import types
from aiogram.dispatcher import filters
from pycbrf import ExchangeRates

from loader import dp, bot
from ..services import (
    get_pyjs_message,
    get_hello_message
)


dollar = ["бакс", "оллар", "$"]


@dp.message_handler(filters.Text(contains="ривет", ignore_case=True))
async def welcome_message(message: types.Message):
    rnd_message = random.choice(get_hello_message())
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{rnd_message} @{message.from_user.username}"
    )


@dp.message_handler(filters.Text(contains="оллар", ignore_case=True))
async def get_dollar(message: types.Message):
    rates = ExchangeRates(
        str(datetime.datetime.now().date()), locale_en=True
    )
    current_usd = f'{rates["USD"].name} - {rates["USD"].value} руб.'
    await message.reply(
        text=current_usd
    )


@dp.message_handler(filters.Text(contains="аксим", ignore_case=True))
async def hello_maxim(message: types.Message):
    sticker = "CAACAgIAAxkBAAEDoflh2CqUHby5Nfyui9G7kaP" \
              "E4AxfrwACHAIAAqzRchNIr_rSmKNEVyME"
    await bot.send_message(
        message.chat.id, text="@kozenkodev СЕКСУАЛЬНЫЙ ГОВНОКОДЕР!!! СОСЕТ ХУЙ"
    )
    await bot.send_sticker(message.chat.id, sticker)
