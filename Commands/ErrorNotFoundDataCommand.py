from aiogram.types import Message

from Commands import ICommand


class ErrorNotFoundDataCommand(ICommand):
    async def execute(self, message: Message) -> None:
        message.answer()