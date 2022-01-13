from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from config import ADMINS


class IsAdmin(BoundFilter):

    async def check(self, message: Message):
        return str(message.from_user.id) in ADMINS