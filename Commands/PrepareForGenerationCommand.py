from aiogram.types import Message

from Commands import ICommand
from Keyboard import ConfirmGenerateKeyboard
from config import max_message_length


class PrepareForGenerationCommand(ICommand):
    text = 'Проверить текст, поменять если надо, нажать на кнопку Сгенерировать. И не задавать лишних вопрос!'

    async def execute(self, message: Message) -> None:
        keyboard = ConfirmGenerateKeyboard().get_keyboard()
        await message.answer(text=self.text, reply_markup=keyboard)
