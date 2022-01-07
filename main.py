import asyncio
import datetime
import logging

import aioschedule
from aiogram import executor

from loader import dp, bot
from config import CHAT_ID
from src import handlers


async def check_birthday():
    a = "2022-01-07".split("-")

    q = datetime.datetime(int(a[0]), int(a[1]), int(a[2])).date()
    w = datetime.datetime.today().date()
    if q == w:
        await bot.send_message(CHAT_ID, text="хуй")


async def scheduler():
    aioschedule.every(1).days.do(check_birthday)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook()


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )
