import asyncio
import logging

import aioschedule
from aiogram import executor

from loader import dp, bot

from src.handlers.birthday import check_birthday
from src import handlers
from src.handlers.simple_message import how_to_day


async def scheduler():
    aioschedule.every(4).hours.do(check_birthday)
    aioschedule.every(3).hours.do(how_to_day)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


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
