import datetime
import json

from config import CHAT_ID, BD_STICKER
from loader import bot


async def check_birthday() -> None:
    """ Проверят дату рожджения с текущей датой
    """
    now = datetime.datetime.today().date()
    with open('src/data/birthday.json', "r") as f:
        list_users = json.load(f).get("users")
        for i in list_users:
            list_date = list(i.keys())
            for key in list_date:
                _now = str(now).split("-", 1)[1]
                _key = key.split("-", 1)[1]
                if _key == _now:
                    await bot.send_message(
                        CHAT_ID,
                        text=f"{i.get(key)}, С днем рождения !!!"
                    )
                    await bot.send_sticker(CHAT_ID, BD_STICKER)
