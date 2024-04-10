from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.Utils import Utils
from bot.Handlers import SessionHandler
from bot.Commands import HelloCommand, PrepareForGenerationCommand
from bot.Commands.ErrorCommands import ErrorMessageLengthExceeded, ErrorMessageWithEnglish
from bot.States import StateList
from bot.config import max_message_length


class SentMessageHandler:
    @staticmethod
    async def handle_start_command(message: Message, state: FSMContext) -> None:
        await HelloCommand().execute(message)
        await SessionHandler.handle_new_session(message, state)

    @staticmethod
    async def handle_initial_text(message: Message, state: FSMContext) -> None:
        if Utils.contains_english_chars(message.text):
            await ErrorMessageWithEnglish().execute(message)
            return

        if len(message.text) > max_message_length:
            await ErrorMessageLengthExceeded().execute(message)
            return

        await state.set_state(StateList.waiting_for_confirmation)
        await PrepareForGenerationCommand().execute(message)
        await state.update_data({
            'initial_text': message.text,
            'initial_text_message_id': message.message_id
        })
