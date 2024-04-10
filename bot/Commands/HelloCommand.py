from aiogram.types import Message

from bot.Commands import ICommand


class HelloCommand(ICommand):
    text = '🎶 Привет! Я твой Музыкальный Мастер Бот 🎵. Я здесь, чтобы превратить твои идеи в музыку.'

    async def execute(self, message: Message) -> None:
        await message.answer(
            text=self.text,
            parse_mode='html')
