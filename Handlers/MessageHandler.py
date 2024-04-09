from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Commands import HelloCommand, NewLoopCommand, PrepareForGenerationCommand
from Commands.ErrorCommands import ErrorMessageLengthExceeded
from States import StateList
from config import default_style_type, max_message_length


class MessageHandler:
    @staticmethod
    async def handle_start_command(message: Message, state: FSMContext) -> None:
        await state.update_data({
            'style_type': default_style_type,
            'audio_mode': True
        })

        await state.set_state(StateList.waiting_for_initial_text)
        await HelloCommand().execute(message)
        await NewLoopCommand(selected_type=default_style_type).execute(message)

    # TODO: Сделать Handler для перезапущенной сессии или новой сессии(SessionHandler)
    @staticmethod
    async def handle_restarted_session(message: Message, state: FSMContext) -> None:
        await state.update_data({
            'style_type': default_style_type,
            'audio_mode': True
        })

        await state.set_state(StateList.waiting_for_initial_text)
        await NewLoopCommand(selected_type=default_style_type).execute(message)

    @staticmethod
    async def handle_initial_text(message: Message, state: FSMContext) -> None:
        if len(message.text) > max_message_length:
            await ErrorMessageLengthExceeded().execute(message)
            return

        await state.set_state(StateList.waiting_for_confirmation)
        await PrepareForGenerationCommand().execute(message)
        await state.update_data({
            'initial_text': message.text,
            'initial_text_message_id': message.message_id
        })

    @staticmethod
    async def handle_edited_initial_text(message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        initial_text_message_id = data.get('initial_text_message_id')

        if message.message_id != initial_text_message_id:
            return

        if len(message.text) > max_message_length:
            await ErrorMessageLengthExceeded().execute(message)
            return

        await state.update_data({
            'initial_text': message.text
        })
