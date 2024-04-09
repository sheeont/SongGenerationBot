from aiogram.types import Message

from Commands import ICommand
from config import max_message_length


class ErrorMessageLengthExceeded(ICommand):
    text = (f'Превышен лимит по размеру текста({max_message_length}), '
            'пожалуйста сократите текст, влезло только:\n\n'
            '{cropped_text}')

    async def execute(self, message: Message) -> None:
        await message.answer(
            self.text.format(cropped_text=message.text[:max_message_length])
        )
