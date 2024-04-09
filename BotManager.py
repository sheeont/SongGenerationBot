from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
import logging

from Handlers import MessageHandler, KeyboardHandler
from States import StateList


class BotManager:
    def __init__(self, token: str, logging_config: logging.BASIC_FORMAT = logging.INFO):
        logging.basicConfig(level=logging_config)

        self.bot = Bot(token=token)
        # TODO: Проверить можно ли сохранять в оперативку
        self.dp = Dispatcher()

        self.setup()

    def setup(self):
        # Обработка отправляемых сообщений
        self.dp.message.register(MessageHandler.handle_start_command, Command('start'))
        self.dp.message.register(
            MessageHandler.handle_initial_text,
            StateFilter(StateList.waiting_for_initial_text)
        )

        # Обработка изменяемых сообщений
        self.dp.edited_message.register(MessageHandler.handle_edited_initial_text, StateFilter(StateList.waiting_for_confirmation))

        # Обработчики перезапущенной сессии
        self.dp.message.register(MessageHandler.handle_restarted_session, StateFilter(None))
        self.dp.callback_query.register(KeyboardHandler.handle_restarted_session, StateFilter(None))

        # Данные обработчики работают только если (State is not None)
        self.dp.callback_query.register(KeyboardHandler.handle_styles, F.data.startswith('style_type'))
        self.dp.callback_query.register(KeyboardHandler.handle_audio_button, F.data == 'main_audio_button')
        self.dp.callback_query.register(KeyboardHandler.handle_generate_button, F.data == 'generate_button')

    async def run(self):
        await self.dp.start_polling(self.bot)
