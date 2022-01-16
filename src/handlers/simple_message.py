import asyncio
import datetime
import random
from contextlib import suppress

from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import CallbackQuery
from pycbrf import ExchangeRates

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
async def welcome_message(message: types.Message):
    rnd_message = random.choice(get_hello_message())
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{rnd_message} @{message.from_user.username}",
        reply_markup=delete_message_keyboard
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


@dp.message_handler(
    filters.Text(contains=["еонид", "енчик"], ignore_case=True)
)
async def start_dialog(message: types.Message):
    await message.answer(f"Че надо? @{message.from_user.username}")


@dp.message_handler(text=["акой язык лучше"])
async def lang_vs_lang(message: types.Message, state: FSMContext):
    lg = random.choice(lang)
    await message.answer(f"На мой взгляд, лучшим языком является: {lg}")
    await state.finish()
