import datetime
import random

from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from pycbrf import ExchangeRates

from loader import dp, bot
from ..filters import IsAdmin
from ..states.leonid_state import DialogIsLeonid
from ..services import (
    get_hello_message
)


dollar = ["бакс", "оллар", "$"]
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


@dp.message_handler(
    # IsAdmin(),
    text=["леонид", "ленчик"],
)
async def start_dialog(message: types.Message):
    await message.answer(f"Че надо? @{message.from_user.username}")
    await DialogIsLeonid.how_are_you.set()


@dp.message_handler(
    # IsAdmin(),
    text=["как дела", "как жизнь"],
    state=DialogIsLeonid.how_are_you
)
async def how_are_you(message: types.Message):
    await message.answer(
        "знаешь брат, дела херня, не хватает оперативы, "
        "инет говно, разраб говно, на говнокодил он меня, "
        "на питоне написали бля, пошли все нахер, мудаки, сосите писю пиздюки",
    )
    await DialogIsLeonid.lang_vs_lang.set()


@dp.message_handler(
    # IsAdmin(),
    text=["какой язык лучше"],
    state=DialogIsLeonid.lang_vs_lang
)
async def lang_vs_lang(message: types.Message, state: FSMContext):
    l = random.choice(lang)
    await message.answer(f"На мой взгляд, лучшим языком является: {l}")
    await state.finish()
