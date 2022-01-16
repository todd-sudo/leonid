from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


delete_message_keyboard = InlineKeyboardMarkup()
delete = InlineKeyboardButton(
    "Удалить",
    callback_data='delete_msg'
)

delete_message_keyboard.add(delete)
