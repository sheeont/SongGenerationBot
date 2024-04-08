from aiogram.types import Message

from Commands.ICommand import ICommand
from Keyboard.MainCancelKeyboard import MainCancelKeyboard


class PromptTextCommand(ICommand):
    # TODO: Поменять текст
    text = (
        '✏️ Пришло время творить! Теперь, когда ты выбрал тип генерации, давай перейдём к самому интересному — созданию'
        ' твоего произведения. Введи начальные строки песни, и я займусь их преобразованием.\n\n'
        'Выбран жанр: {style_name}\n\n'
        'Если захочешь отменить или начать сначала, просто нажми кнопку "Отмена" ниже.')

    def __init__(self, style_name: str):
        self.style_name = style_name

    async def execute(self, message: Message) -> None:
        keyboard = MainCancelKeyboard().get_keyboard()

        text = self.text.format(style_name=self.style_name)
        await message.edit_text(text=text, reply_markup=keyboard, parse_mode='html')
