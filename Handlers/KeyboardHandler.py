from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from Commands.NewLoopCommand import NewLoopCommand
from Commands.PromptTextCommand import PromptTextCommand
from config import styles_data


class KeyboardHandler:
    @staticmethod
    async def handle_styles(callback: CallbackQuery, state: FSMContext) -> None:
        style_type = callback.data.split('_')[2]

        await state.update_data({
            'style_type': style_type
        })

        # Получаем название жанра: Рэп, Поп...
        style_name = ''
        for style in styles_data:
            style_text = style['text']
            style_callback_data = style['callback_data']

            if style_callback_data == style_type:
                style_name = style_text

        await PromptTextCommand(style_name).execute(callback.message)

    @staticmethod
    async def handle_main_cancel(callback: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        await NewLoopCommand(
            data.get('style_type', styles_data[0]['callback_data']),
            True,
            data.get('audio_mode', True)
        ).execute(callback.message)

    @staticmethod
    async def handle_audio_button(callback: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()

        # Получаем текущее значение режима
        audio_mode: bool = data.get('audio_mode', True)
        # Изменяем значение режима
        audio_mode = not audio_mode

        await NewLoopCommand(
            data.get('style_type', styles_data[0]['callback_data']),
            True,
            audio_mode
        ).execute(callback.message)

        await state.update_data({
            'audio_mode': audio_mode
        })
