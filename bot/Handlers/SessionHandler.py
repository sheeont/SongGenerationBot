from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.Commands import NewLoopCommand, NotifyDevelopmentStatusCommand
from bot.States import StateList
from bot.config import default_style_type


class SessionHandler:
    @staticmethod
    async def handle_new_session(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
        if isinstance(message, CallbackQuery):
            message = message.message

        await state.update_data({
            'style_type': default_style_type,
            'audio_mode': True
        })

        await state.set_state(StateList.waiting_for_initial_text)
        await NewLoopCommand(selected_type=default_style_type).execute(message)

    @staticmethod
    async def handle_development_mode_session(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
        if isinstance(message, CallbackQuery):
            message = message.message

        await NotifyDevelopmentStatusCommand().execute(message)
