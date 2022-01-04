import datetime
import logging

from aiogram import executor, types
from pycbrf import ExchangeRates

from loader import dp, bot
from src import handlers


async def on_startup(dp):
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
