from aiogram.types import Message

from bot.Commands import ICommand


class NotifyDevelopmentStatusCommand(ICommand):
    text = '🤖Сейчас бот усердно работает над собой и улучшает свои навыки🛠️.\n✨Скоро будем на связи!'

    async def execute(self, message: Message) -> None:
        await message.answer(
            text=self.text,
            parse_mode='html')
