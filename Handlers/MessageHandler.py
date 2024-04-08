from aiogram.types import Message

from Commands.Message.HelloCommand import HelloCommand


class MessageHandler:
    @staticmethod
    async def start_command(message: Message) -> None:
        await HelloCommand().execute(message)
