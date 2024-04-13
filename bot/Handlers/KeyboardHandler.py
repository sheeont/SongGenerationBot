from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.Commands import NewLoopCommand, ContentDeliveryCommand
from bot.config import default_style_type
from bot.States import StateList

from bot.Handlers.SessionHandler import SessionHandler


class KeyboardHandler:
    @staticmethod
    async def handle_styles(callback: CallbackQuery, state: FSMContext) -> None:
        style_type = callback.data.split('_')[2]

        data = await state.get_data()
        previous_style_type = data.get('style_type', '')
        audio_mode = data.get('audio_mode', True)

        if previous_style_type == style_type:
            await callback.answer()
            return

        await state.update_data({
            'style_type': style_type
        })

        await NewLoopCommand(style_type, True, audio_mode).execute(callback.message)

    @staticmethod
    async def handle_audio_button(callback: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        style_type = data.get('style_type', default_style_type)

        # Получаем текущее значение режима
        audio_mode: bool = data.get('audio_mode', True)
        # Изменяем значение режима
        audio_mode = not audio_mode

        await state.update_data({
            'audio_mode': audio_mode
        })

        await NewLoopCommand(style_type, True, audio_mode).execute(callback.message)

    @staticmethod
    async def handle_generate_button(callback: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()

        style_type = data.get('style_type')
        audio_mode = data.get('audio_mode')
        initial_text = data.get('initial_text')

        await ContentDeliveryCommand(style_type, audio_mode, initial_text).execute(callback.message)
        await state.set_state(StateList.waiting_for_initial_text)

        await SessionHandler.handle_new_session(callback, state)
