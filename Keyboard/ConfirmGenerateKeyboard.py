from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Keyboard import IKeyboard


class ConfirmGenerateKeyboard(IKeyboard):
    def get_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton(text='Сгенерировать', callback_data='generate_button')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        return keyboard
