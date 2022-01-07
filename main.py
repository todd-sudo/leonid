import asyncio
import datetime
import logging
import json

import aioschedule
from aiogram import executor

from loader import dp, bot
from config import CHAT_ID, BD_STICKER
from src import handlers


async def check_birthday():
    """ Проверят дату рожджения с текущей датой
    """
    now = datetime.datetime.today().date()

    with open('src/data/birthday.json', "r") as f:
        list_users = json.load(f).get("users")
        for i in list_users:
            list_date = list(i.keys())
            for key in list_date:
                if key == str(now):
                    new_key = key.split("-")
                    bd = datetime.datetime(
                        int(new_key[0]), int(new_key[1]), int(new_key[2])
                    ).date()
                    if bd == now:
                        await bot.send_message(
                            CHAT_ID,
                            text=f"[ХУЙ] С днем рождения, {i.get(key)}!!!🎂 [ХУЙ]"
                        )
                        await bot.send_sticker(CHAT_ID, BD_STICKER)


async def scheduler():
    aioschedule.every(1).days.do(check_birthday)
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
