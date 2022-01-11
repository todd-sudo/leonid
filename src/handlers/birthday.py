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
                _now = str(now).split("-")
                print(_now)
                _now = now[1] + now[2]
                _key = key.split("-")
                _key = key[1] + key[2]
                if _key == _now:
                    print(True)
                    await bot.send_message(
                        CHAT_ID,
                        text=f"[ХУЙ] С днем рождения, {i.get(key)}!!!🎂 [ХУЙ]"
                    )
                    await bot.send_sticker(CHAT_ID, BD_STICKER)
