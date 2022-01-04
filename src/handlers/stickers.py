from aiogram import types

from loader import dp, bot
from ..services import get_python, get_ios, get_windows, get_thanks, get_js


@dp.message_handler(text=["python", "питон", "Python", "питончик"])
async def python_text(message: types.Message):
    await bot.send_sticker(sticker=f"{get_python()}", chat_id=message.chat.id)


@dp.message_handler(text=["ios", "Айфон", "айфон"])
async def ios_text(message: types.Message):
    await bot.send_sticker(sticker=f"{get_ios()}", chat_id=message.chat.id)


@dp.message_handler(text=["windows", "винда", "Винда", "Windows"])
async def windows_text(message: types.Message):
    await bot.send_sticker(sticker=f"{get_windows()}", chat_id=message.chat.id)


@dp.message_handler(text=["Спасибо", "спасибо"])
async def thanks_text(message: types.Message):
    await bot.send_sticker(sticker=f"{get_thanks()}", chat_id=message.chat.id)


@dp.message_handler(text=["js", "джс", "JS"])
async def js_text(message: types.Message):
    await bot.send_sticker(sticker=f"{get_js()}", chat_id=message.chat.id)
