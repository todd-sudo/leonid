import json
import os.path
import random

import requests
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery
from aiogram.types.inline_keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from bs4 import BeautifulSoup
from loader import dp, bot
import config
from .keyboards import delete_message_keyboard, get_callback_data_p_name
from .text import leonid_text, hello, anya_list
from .utils import delete_all_files_in_folder_bird, save_data_username_in_file_bird, \
    get_data_in_file_bird
from ..bird.bird import find_username


cb = get_callback_data_p_name()


@dp.callback_query_handler(cb.filter())
async def get_info_on_username(call: types.CallbackQuery, callback_data: dict):
    await call.answer("Информация загружается")
    sites = get_data_in_file_bird()
    if not sites:
        await call.message.answer("Нет сохраненных данных!")
    app_name = callback_data["p_name"]
    for site in sites:
        site_lower_name = site.get("app").lower()
        if app_name == site_lower_name:
            msg = f"Статус: {site.get('status')}\n" \
                  f"Соц. сеть: {site.get('app')}\n" \
                  f"Ссылка: {site.get('url')}\n"
            await call.message.answer(msg)


@dp.message_handler(filters.Text(contains="найди:", ignore_case=True))
async def find_username_handler(message: types.Message):
    delete_all_files_in_folder_bird()
    u_message = message.text.strip().split(":")
    if len(u_message) != 2:
        await message.answer("Невалидный текст")
        return
    msg = await message.answer("Ищу...")
    username = u_message[1].strip()
    data = await find_username(username=username)
    if not data:
        await message.answer("Произошла ошибка")
        return
    sites = data.get("sites")
    buttons = InlineKeyboardMarkup(row_width=6)
    btns = []
    save_data_username_in_file_bird(sites, username)
    for s in sites:
        print(s.get("app"))
        if s.get("status") != "FOUND":
            continue
        btn = InlineKeyboardButton(
            text=s.get("app"),
            callback_data=cb.new(p_name=s.get("app").lower())
        )
        btns.append(btn)

    for b in btns:
        buttons.add(b)
    await message.answer(username, reply_markup=buttons)
    await bot.delete_message(message.chat.id, msg.message_id)


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
    if message.from_user.id == config.ADMINS[2]:
        path = "src/data/state/"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + "state.json", "w") as f:
            json.dump({"state": True}, f, indent=4, ensure_ascii=False)

        await message.answer("Ок бро! Включил админ режим!")


@dp.message_handler(filters.Text(contains=["вырубай"], ignore_case=True))
async def off_admin(message: types.Message):
    if message.from_user.id == config.ADMINS[2]:
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
    if state and message.from_user.id != config.ADMINS[2]:
        return
    rnd_message = random.choice(leonid_text)
    await message.answer(
        text=f"{rnd_message}",
    )


@dp.message_handler(filters.Text(contains=["аня"], ignore_case=True))
async def anya(message: types.Message):
    state = get_state()
    if state and message.from_user.id != config.ADMINS[2]:
        return
    msg = random.choice(anya_list)
    await message.answer(text=msg)


@dp.message_handler(filters.Text(contains=["анька"], ignore_case=True))
async def anya2(message: types.Message):
    state = get_state()
    if state and message.from_user.id != config.ADMINS[2]:
        return
    msg = random.choice(anya_list)
    await message.answer(text=msg)


@dp.message_handler(filters.Text(contains=["анюта"], ignore_case=True))
async def anya3(message: types.Message):
    state = get_state()
    if state and message.from_user.id != config.ADMINS[2]:
        return
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
    state = get_state()
    if state and message.from_user.id != config.ADMINS[2]:
        return
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
