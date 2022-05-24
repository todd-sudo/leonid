import asyncio
from email.message import Message
import os.path
import random
import socket
import uuid
import time

import requests
import qrcode
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery
from bs4 import BeautifulSoup

from config import GPU
from loader import dp, bot
from .keyboards import delete_message_keyboard
from ..filters import IsAdmin

lang = [
    "Java",
    "С",
    "Go",
    "C#",
    "JavaScript",
    "РНР",
    "Ruby",
]

hello = [
    "Привет",
    "Дарова",
    "Здарова",
    "Че надо?",
    "Приветули",
    "Силям Алейкум"
]

leonid_text = [
    "Да-да..",
    "Чего тебе?",
    "Отвали...",
    "Ну что опять?",
    "Шо такое?",
    "Не трогай меня",
    "Что такое?",
    "Я тут",
]


# async def how_do_you_do():
#     for ch_id in [-1001261470613, -1001383004405, -688082212]:
#         await bot.send_message(ch_id, f"Как дела?")


@dp.callback_query_handler(text="delete_msg")
async def delete_bot_message(call: CallbackQuery):
    msg = call.message.message_id
    await bot.delete_message(call.message.chat.id, msg)
    msg = await call.message.answer(f"@{call.from_user.username} ты че обалдел?")
    await asyncio.sleep(5)
    await bot.delete_message(call.message.chat.id, msg.message_id)


@dp.message_handler(filters.Text(contains=["леонид"], ignore_case=True))
async def leonid(message: types.Message):
    rnd_message = random.choice(leonid_text)
    await message.answer(
        text=f"{rnd_message} @{message.from_user.username}",
        reply_markup=delete_message_keyboard
    )


@dp.message_handler(IsAdmin(), commands=['about'])
async def welcome_message(message: types.Message):
    await message.answer("""
Мои команды: 
1. доллар | /dollar - показывать курс доллар в рублях
2. яп | /lang - рандомно показывать лучший ЯП
3. /site_ip:google.com - показывать IP адрес сайта(после двоеточия)
4. /qr:https://google.com - заворачивать ссылки в QR код(обязательно наличие http's)
5. imgrus, imgen, imgua + ФОТО С ТЕКСТОМ - считывать текст с фотографии:
    imgrus - русский
    imgen - английский
    imgua - украинский
    """)


@dp.message_handler(filters.Text(contains="ривет", ignore_case=True))
@dp.message_handler(commands=['hello'])
async def welcome_message(message: types.Message):
    rnd_message = random.choice(hello)
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
    r = requests.get("https://ru.investing.com/currencies/usd-rub",
                     headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    data = soup.find("span", class_="text-2xl").text.strip()
    await message.answer(data)


@dp.message_handler(commands=['lang'])
@dp.message_handler(filters.Text(contains=["яп"], ignore_case=True))
async def lang_vs_lang(message: types.Message):
    lg = random.choice(lang)
    await message.answer(f"На мой взгляд, лучшим языком является {lg}")


@dp.message_handler(filters.Text(contains=["/site_ip:"], ignore_case=True))
async def get_site_ip(message: types.Message):
    host = message.text.split(":")[1]
    try:
        ip_address = socket.gethostbyname(host)
        if ip_address is not None:
            await message.answer(
                f"Host Name: {host}\nIP Address: {ip_address}")
    except Exception:
        await message.answer("Invalid hostname...")


@dp.message_handler(filters.Text(contains=["/qr:"], ignore_case=True))
async def generate_qrcode(message: types.Message):
    path = "src/data/qrcodes"
    if not os.path.exists(path):
        os.makedirs(path)
    string = message.text

    qr = qrcode.make(string)
    image_name = f"{uuid.uuid4()}.png"
    qr.save(stream=f"{path}/{image_name}")

    with open(f"{path}/{image_name}", "rb") as file:
        await bot.send_photo(message.chat.id, file)
    os.remove(f"{path}/{image_name}")

