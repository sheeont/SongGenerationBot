from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Keyboard.IKeyboard import IKeyboard


class MainCancelKeyboard(IKeyboard):
    def get_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [[InlineKeyboardButton(text='Отмена', callback_data='main_cancel')]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
