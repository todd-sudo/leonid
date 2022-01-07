import datetime
import json

from config import CHAT_ID, BD_STICKER
from loader import bot


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
