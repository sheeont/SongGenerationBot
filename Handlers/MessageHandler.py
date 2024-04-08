from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Commands import HelloCommand, NewLoopCommand, PrepareForGenerationCommand
from States import StateList
from config import styles_data


class MessageHandler:
    @staticmethod
    async def start_command(message: Message, state: FSMContext) -> None:
        await state.clear()
        await HelloCommand().execute(message)
        await NewLoopCommand(selected_type=styles_data[0]['callback_data']).execute(message)

    @staticmethod
    async def prepare_for_generation_command(message: Message, state: FSMContext) -> None:
        await state.set_state(StateList.text_editing_state)

        await state.update_data({
            'generation_trigger_message_id': message.message_id
        })

        await PrepareForGenerationCommand().execute(message)
