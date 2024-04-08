from aiogram.types import Message

from Keyboard import MainKeyboard
from Commands import ICommand
from config import styles_data


class HelloCommand(ICommand):
    # TODO: Поменять имя бота
    text = '🎶 Привет! Я твой Музыкальный Мастер Бот 🎵. Я здесь, чтобы превратить твои идеи в музыку.'

    async def execute(self, message: Message) -> None:
        await message.answer(
            text=self.text,
            parse_mode='html')
