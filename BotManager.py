from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
import logging

from Handlers.MessageHandler import MessageHandler
from Handlers.KeyboardHandler import KeyboardHandler


class BotManager:
    def __init__(self, token: str, logging_config: logging.BASIC_FORMAT = logging.INFO):
        logging.basicConfig(level=logging_config)

        self.bot = Bot(token=token)
        self.dp = Dispatcher()

        self.setup()

    def setup(self):
        self.dp.message.register(MessageHandler.start_command, Command('start'))
        self.dp.callback_query.register(KeyboardHandler.handle_styles, F.data.startswith('style_type'))
        self.dp.callback_query.register(KeyboardHandler.handle_styles, F.data.startswith('style_type'))
        self.dp.callback_query.register(KeyboardHandler.handle_audio_button, F.data == 'main_audio_button')
        self.dp.callback_query.register(KeyboardHandler.handle_main_cancel, F.data == 'main_cancel')

    async def run(self):
        await self.dp.start_polling(self.bot)
