import datetime
import random

from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery
from pycbrf import ExchangeRates

from config import CHAT_ID
from loader import dp, bot
from .keyboards import delete_message_keyboard
from ..services import (
    get_hello_message
)


lang = [
    "Java",
    "С",
    "Python",
    "C++",
    "Go",
    "C#",
    "JavaScript",
    "РНР",
]


@dp.callback_query_handler(text="delete_msg")
async def delete_bot_message(call: CallbackQuery):
    msg = call.message.message_id
    await bot.delete_message(call.message.chat.id, msg)


@dp.message_handler(filters.Text(contains="ривет", ignore_case=True))
@dp.message_handler(commands=['hello'])
async def welcome_message(message: types.Message):
    rnd_message = random.choice(get_hello_message())
    print(message.chat.id)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"{rnd_message} @{message.from_user.username}",
        reply_markup=delete_message_keyboard
    )


@dp.message_handler(filters.Text(contains="оллар", ignore_case=True))
@dp.message_handler(commands=['dollar'])
async def get_dollar(message: types.Message):
    rates = ExchangeRates(
        str(datetime.datetime.now().date()), locale_en=True
    )
    current_usd = f'{rates["USD"].name} - {rates["USD"].value} руб.'
    await bot.send_message(
        CHAT_ID,
        text=current_usd
    )


@dp.message_handler(filters.Text(contains=["еонид"], ignore_case=True))
@dp.message_handler(commands=['leonid'])
async def start_dialog(message: types.Message):
    await bot.send_message(CHAT_ID, f"Че надо? @{message.from_user.username}")


@dp.message_handler(filters.Text(contains=["акой язык лучше"], ignore_case=True))
@dp.message_handler(commands=['lang'])
async def lang_vs_lang(message: types.Message):
    lg = random.choice(lang)
    await bot.send_message(CHAT_ID, f"На мой взгляд, лучшим языком является: {lg}")
