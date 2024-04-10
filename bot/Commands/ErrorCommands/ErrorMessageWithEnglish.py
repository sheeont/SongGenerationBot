from aiogram.types import Message

from bot.Commands import ICommand


class ErrorMessageWithEnglish(ICommand):
    text = 'Упс! Пожалуйста, давайте придерживаться русских символов 😊'

    async def execute(self, message: Message) -> None:
        await message.answer(text=self.text)
