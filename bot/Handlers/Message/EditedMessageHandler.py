from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.Commands.ErrorCommands import ErrorMessageLengthExceeded, ErrorMessageWithEnglish
from bot.config import max_message_length
from bot.Utils import Utils


class EditedMessageHandler:
    @staticmethod
    async def handle_edited_initial_text(message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        initial_text_message_id = data.get('initial_text_message_id')

        if message.message_id != initial_text_message_id:
            return

        if Utils.contains_english_chars(message.text):
            await ErrorMessageWithEnglish().execute(message)
            return

        if len(message.text) > max_message_length:
            await ErrorMessageLengthExceeded().execute(message)
            return

        await state.update_data({
            'initial_text': message.text
        })
