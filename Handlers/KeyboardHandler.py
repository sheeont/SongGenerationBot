from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from Commands import NewLoopCommand, ContentDeliveryCommand
from config import styles_data
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
        style_type = data.get('style_type', styles_data[0]['callback_data'])

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
        message = callback.message
        data = await state.get_data()

        style_type = data.get('style_type', None)
        audio_mode = data.get('audio_mode', False)

        # TODO: Проверить достаточно ли просто проверки на style_type
        if style_type is None:
            await NewLoopCommand(styles_data[0]['callback_data']).execute(message)
            return

        await state.set_state(StateList.generate_content_state)

        await ContentDeliveryCommand(audio_mode).execute(message)

        await state.set_state(StateList.wait_text_enter_state)
