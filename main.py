import asyncio
import logging

import aioschedule
from aiogram import executor

from config import TIME
from loader import dp, bot

from src.handlers.birthday import check_birthday


async def scheduler():
    # aioschedule.every(1).days.at(TIME).do(check_birthday)
    aioschedule.every(5).seconds.do(check_birthday)
    while True:
        await aioschedule.run_pending()
#        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
    # logging.basicConfig(level=logging.INFO)
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
