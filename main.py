import asyncio
import logging

import aioschedule
from aiogram import executor

from loader import dp, bot

from src.handlers.birthday import check_birthday
from src.handlers.message import get_eat
from src import handlers


async def scheduler():
    aioschedule.every(1).hours.do(check_birthday)
    aioschedule.every(10).minutes.do(get_eat)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
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
