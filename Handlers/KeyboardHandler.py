from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from Commands import NewLoopCommand, ContentDeliveryCommand
from config import styles_data, default_style_type
from States import StateList


class KeyboardHandler:
    @staticmethod
    async def handle_styles(callback: CallbackQuery, state: FSMContext) -> None:
        style_type = callback.data.split('_')[2]

        data = await state.get_data()
        audio_mode = data.get('audio_mode', True)

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

        # TODO: Интегрировать класс обработчик для перезапущенной сессии или новой сессии(SessionHandler)
        await state.update_data({
            'style_type': default_style_type,
            'audio_mode': True
        })

        await state.set_state(StateList.waiting_for_initial_text)
        await NewLoopCommand(default_style_type).execute(callback.message)

    @staticmethod
    async def handle_restarted_session(callback: CallbackQuery, state: FSMContext) -> None:
        await state.update_data({
            'style_type': default_style_type,
            'audio_mode': True
        })

        await state.set_state(StateList.waiting_for_initial_text)
        await NewLoopCommand(default_style_type).execute(callback.message)
