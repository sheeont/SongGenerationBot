from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter, BaseFilter
import logging

from Handlers import SessionHandler, KeyboardHandler
from Handlers.Message import SentMessageHandler, EditedMessageHandler
from States import StateList
from bot.CustomFilters import IsDevelopmentFilter


class BotManager:
    def __init__(self, token: str, logging_config: logging.BASIC_FORMAT = logging.INFO):
        logging.basicConfig(level=logging_config)

        self.bot = Bot(token=token)
        # TODO: Проверить можно ли сохранять в оперативку
        self.dp = Dispatcher()

        self.setup()

    def setup(self) -> None:
        # Обработка режима разработки
        self.dp.message.register(SessionHandler.handle_development_mode_session, IsDevelopmentFilter())
        self.dp.edited_message.register(SessionHandler.handle_development_mode_session, IsDevelopmentFilter())
        self.dp.callback_query.register(SessionHandler.handle_development_mode_session, IsDevelopmentFilter())

        # Обработка отправляемых сообщений
        self.dp.message.register(SentMessageHandler.handle_start_command, Command('start'))
        self.dp.message.register(
            SentMessageHandler.handle_initial_text,
            StateFilter(StateList.waiting_for_initial_text)
        )

        # Обработка изменяемых сообщений
        self.dp.edited_message.register(EditedMessageHandler.handle_edited_initial_text,
                                        StateFilter(StateList.waiting_for_confirmation))

        # Обработчики перезапущенной сессии
        self.dp.message.register(SessionHandler.handle_new_session, StateFilter(None))
        self.dp.callback_query.register(SessionHandler.handle_new_session, StateFilter(None))

        # Данные обработчики работают только если (State is not None)
        self.dp.callback_query.register(KeyboardHandler.handle_styles, F.data.startswith('style_type'))
        self.dp.callback_query.register(KeyboardHandler.handle_audio_button, F.data == 'main_audio_button')
        self.dp.callback_query.register(KeyboardHandler.handle_generate_button, F.data == 'generate_button')

    async def run(self) -> None:
        await self.dp.start_polling(self.bot)
