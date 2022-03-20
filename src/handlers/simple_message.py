import random
import socket

import requests
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery
from bs4 import BeautifulSoup

from config import CHAT_ID
from loader import dp, bot
from .keyboards import delete_message_keyboard
from ..services import (
    get_hello_message,
)


lang = [
    "Java",
    "С",
    "C++",
    "Go",
    "C#",
    "JavaScript",
    "РНР",
    "Pascal",
    "Ruby",
    "Basic"
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


@dp.message_handler(commands=['lang'])
@dp.message_handler(filters.Text(contains=["яп"], ignore_case=True))
async def lang_vs_lang(message: types.Message):
    lg = random.choice(lang)
    await message.answer(f"На мой взгляд, лучшим языком является {lg}")


async def how_to_day():
    await bot.send_message(CHAT_ID, "Как дела?")


@dp.message_handler(filters.Text(contains=["бравис"], ignore_case=True))
async def bravis_hello(message: types.Message):
    await message.answer("bravis one love")


@dp.message_handler(filters.Text(contains=["/site_ip:"], ignore_case=True))
async def get_site_ip(message: types.Message):
    host = message.text.split(":")[1]
    try:
        ip_address = socket.gethostbyname(host)
        if ip_address is not None:
            await message.answer(f"Host Name: {host}\nIP Address: {ip_address}")
    except Exception:
        await message.answer("Invalid hostname...")
