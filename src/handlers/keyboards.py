from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


delete_message_keyboard = InlineKeyboardMarkup()
delete = InlineKeyboardButton(
    "Удалить",
    callback_data='delete_msg'
)

delete_message_keyboard.add(delete)


def get_callback_data_p_name():
    cb = CallbackData("p", "p_name")
    return cb

