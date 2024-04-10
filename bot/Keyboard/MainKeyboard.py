from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.Keyboard import IKeyboard
from bot.config import styles_data


class MainKeyboard(IKeyboard):
    audio_button_text = {
        True: 'Без Аудио',
        False: 'С Аудио'
    }

    def __init__(self, selected_type: str, audio_mode: bool = True):
        self.selected_type = selected_type
        self.audio_mode = audio_mode

    def get_keyboard(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for style in styles_data:
            builder.add(InlineKeyboardButton(
                text=f'{style["text"]} {"✅" if self.selected_type == style["callback_data"] else ""}',
                callback_data=f'style_type_{style["callback_data"]}'
            ))

        builder.adjust(2)
        builder.row(
            InlineKeyboardButton(
                text=f'{self.audio_button_text[self.audio_mode]}',
                callback_data='main_audio_button'
            ),
            width=1
        )

        return builder.as_markup()
