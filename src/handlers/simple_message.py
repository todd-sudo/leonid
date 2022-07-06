import asyncio
import os.path
import random
import uuid

import requests
import qrcode
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery
from bs4 import BeautifulSoup
from loader import dp, bot
import config
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
    "Давай ебаца",
    "Раздевайся дорогуша)"
]

anya_list = [
    "Анюта самая пиздатая",
    "Люблю Аньку)",
    "Анька моя бля!",
    "Кофе с любовью)",
    "Устроим покур!",
    "Аня счастье всей моей жизни!",
    "Солнце мое!",
    "Кисуля))))))))))))))"
]


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
        # reply_markup=delete_message_keyboard
    )


@dp.message_handler(IsAdmin())
async def admin(message: types.Message):
    chid = -736694296
    if message.chat.id == 939392408:
        await bot.send_message(chid, message.text)


@dp.message_handler(filters.Text(contains=["аня"], ignore_case=True))
async def anya(message: types.Message):
    msg = random.choice(anya_list)
    await message.answer(text=msg)


@dp.message_handler(filters.Text(contains=["анька"], ignore_case=True))
async def anya2(message: types.Message):
    msg = random.choice(anya_list)
    await message.answer(text=msg)


@dp.message_handler(filters.Text(contains=["анюта"], ignore_case=True))
async def anya3(message: types.Message):
    msg = random.choice(anya_list)
    await message.answer(text=msg)


async def anekdot():
    url = "https://www.anekdot.ru/"
    res = requests.get(url)
    if res.status_code != 200:
        print("error")
    data = res.text
    if not data:
        print("error")
    soup = BeautifulSoup(data, "lxml")
    divs = soup.find_all("div", class_="text")
    rnd_message = random.choice(divs)
    text = rnd_message.text.strip()
    for chid in config.CHAT_IDS:
        await bot.send_message(chat_id=int(chid), text=text, reply_markup=delete_message_keyboard)


@dp.message_handler(filters.Text(contains="ривет", ignore_case=True))
@dp.message_handler(commands=['hello'])
async def welcome_message(message: types.Message):
    rnd_message = random.choice(hello)
    await message.answer(
        text=f"{rnd_message} @{message.from_user.username}",
        # reply_markup=delete_message_keyboard
    )


@dp.message_handler(filters.Text(contains="оллар", ignore_case=True))
async def get_dollar(message: types.Message):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
    }
    r = requests.get("https://ru.investing.com/currencies/usd-rub",
                     headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    data = soup.find("span", class_="text-2xl").text.strip()
    await message.answer(data)


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

