from aiogram.dispatcher.filters.state import StatesGroup, State


class DialogIsLeonid(StatesGroup):
    """ Стейт для диалога с Леонидом
    """
    how_are_you = State()
    lang_vs_lang = State()
