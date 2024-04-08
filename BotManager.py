from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
import logging

from Handlers import MessageHandler, KeyboardHandler
from States import StateList


class BotManager:
    def __init__(self, token: str, logging_config: logging.BASIC_FORMAT = logging.INFO):
        logging.basicConfig(level=logging_config)

        self.bot = Bot(token=token)
        self.dp = Dispatcher()

        self.setup()

    def setup(self):
        self.dp.message.register(MessageHandler.start_command, Command('start'))
        self.dp.message.register(MessageHandler.prepare_for_generation_command, StateFilter(None))

        self.dp.callback_query.register(KeyboardHandler.handle_styles, F.data.startswith('style_type'))
        self.dp.callback_query.register(KeyboardHandler.handle_audio_button, F.data == 'main_audio_button')
        self.dp.callback_query.register(KeyboardHandler.handle_generate_button, F.data == 'generate_button')

    async def run(self):
        await self.dp.start_polling(self.bot)
