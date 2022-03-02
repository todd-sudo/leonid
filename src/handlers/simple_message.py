import datetime
import time
import random
import asyncio

import requests
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery
from pycbrf import ExchangeRates
from bs4 import BeautifulSoup

from config import CHAT_ID
from loader import dp, bot
from src.filters import IsAdmin
from .keyboards import delete_message_keyboard
from ..services import (
    get_hello_message,
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
    await message.answer(
        text=f"{rnd_message} @{message.from_user.username}",
        reply_markup=delete_message_keyboard
    )


@dp.message_handler(filters.Text(contains="оллар", ignore_case=True))
@dp.message_handler(commands=['dollar'])
async def get_dollar(message: types.Message):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
    }
    r = requests.get("https://ru.investing.com/currencies/usd-rub", headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    data = soup.find("span", class_="text-2xl").text.strip()
    await message.answer(data)


@dp.message_handler(filters.Text(contains=["еонид"], ignore_case=True))
@dp.message_handler(commands=['leonid'])
async def start_dialog(message: types.Message):
    await message.answer(f"Че надо? @{message.from_user.username}")


@dp.message_handler(filters.Text(contains=["акой язык лучше"], ignore_case=True))
@dp.message_handler(commands=['lang'])
async def lang_vs_lang(message: types.Message):
    lg = random.choice(lang)
    await message.answer(f"На мой взгляд, лучшим языком является: {lg}")


@dp.message_handler(filters.Text(contains=["хуй"], ignore_case=True))
async def penis(message: types.Message):
    if message.from_user.id == 559367670:
        await message.reply("Дай деняг!)")
    else:
        msg = random.choice([
            "сам хуй!",
            "не матерись падла!",
            "я за тобой слежу)",
            "щас как уе*ууу тебя!",
            "чик чик!!!",
            "щас до играешся!!!",
        ])
        await message.answer(f"@{message.from_user.username} {msg}")


@dp.message_handler(IsAdmin())
async def admin_message(message: types.Message):
    if message.chat.id == 939392408:
        await bot.send_message(CHAT_ID, message.text)

