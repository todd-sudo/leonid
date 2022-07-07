import json
import os.path
import random

import requests
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery
from bs4 import BeautifulSoup
from loader import dp, bot
import config
from .keyboards import delete_message_keyboard
from .text import leonid_text, hello, anya_list
from ..filters import IsAdmin


ADMIN_MESSAGE = "Не не не)) Включен админ режим!"


def create_first_state():
    path = "src/data/state/"
    with open(path + "state.json", "w") as f:
        json.dump({"state": False}, f, indent=4, ensure_ascii=False)


def get_state() -> bool:
    path = "src/data/state/"
    if not os.path.exists(path):
        os.makedirs(path)
    data = None
    try:
        with open(path + "state.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        create_first_state()
    if not data:
        create_first_state()
        with open(path + "state.json", "r") as f:
            data = json.load(f)
    state = data.get("state")
    return state


@dp.message_handler(filters.Text(contains=["врубай"], ignore_case=True))
async def on_admin(message: types.Message):
    if message.chat.id == config.ADMINS[1]:
        path = "src/data/state/"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + "state.json", "w") as f:
            json.dump({"state": True}, f, indent=4, ensure_ascii=False)

        await message.answer("Ок бро! Включил админ режим!")


@dp.message_handler(filters.Text(contains=["вырубай"], ignore_case=True))
async def off_admin(message: types.Message):
    if message.chat.id == config.ADMINS[1]:
        path = "src/data/state/"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + "state.json", "w") as f:
            json.dump({"state": False}, f, indent=4, ensure_ascii=False)

        await message.answer("Ок бро! Выключил админ режим!")


@dp.callback_query_handler(text="delete_msg")
async def delete_bot_message(call: CallbackQuery):
    msg = call.message.message_id
    await bot.delete_message(call.message.chat.id, msg)


@dp.message_handler(filters.Text(contains=["леонид"], ignore_case=True))
async def leonid(message: types.Message):
    state = get_state()
    print(state)
    if state:
        await message.answer(ADMIN_MESSAGE)
        return
    rnd_message = random.choice(leonid_text)
    await message.answer(
        text=f"{rnd_message}",
    )


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
        await bot.send_message(
            chat_id=int(chid), text=text, reply_markup=delete_message_keyboard
        )


@dp.message_handler(filters.Text(contains="ривет", ignore_case=True))
@dp.message_handler(commands=['start', 'hello'])
async def welcome_message(message: types.Message):
    rnd_message = random.choice(hello)
    await message.answer(
        text=f"{rnd_message} @{message.from_user.username}",
        # reply_markup=delete_message_keyboard
    )


@dp.message_handler(filters.Text(contains="оллар", ignore_case=True))
async def get_dollar(message: types.Message):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0)"
                      " Gecko/20100101 Firefox/97.0"
    }
    r = requests.get(
        "https://ru.investing.com/currencies/usd-rub",
         headers=headers
    )
    soup = BeautifulSoup(r.text, "lxml")
    data = soup.find("span", class_="text-2xl").text.strip()
    await message.answer(data)
