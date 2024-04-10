from aiogram.types import Message

from bot.Commands import ICommand
from bot.Keyboard import ConfirmGenerateKeyboard


class PrepareForGenerationCommand(ICommand):
    text = ('✍️ <b>Если хочешь внести изменения</b> - просто отредактируй своё сообщение. '
            'Когда всё будет готово - нажми кнопку \'Сгенерировать\' ниже. Жду твоего решения! 🚀')

    async def execute(self, message: Message) -> None:
        keyboard = ConfirmGenerateKeyboard().get_keyboard()
        await message.answer(text=self.text, reply_markup=keyboard, parse_mode='html')
