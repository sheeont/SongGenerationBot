from os import remove

from aiogram.types import Message, FSInputFile

from Commands import ICommand
from Content import TextContentGenerator, AudioContentGenerator


# TODO: Перепроверить
class ContentDeliveryCommand(ICommand):
    errors = {
        'TextGenerationFailed': 'Произошла ошибка при генерации текста',
        'AudioGenerationFailed': 'Произошла ошибка при генерации аудио'
    }

    start_generation_message = 'Генерация...\nПожалуйста, подождите'
    finish_generation_message = ('Сгенерированный текст:\n\n'
                                 '{generated_text}')

    def __init__(self, style_type: str, audio_mode: bool, initial_text: str):
        self.style_type = style_type
        self.audio_mode = audio_mode
        self.initial_text = initial_text

    async def handle_text_content(self, message: Message) -> str:
        generated_text = await TextContentGenerator(self.style_type, self.initial_text).generate_content(message.text)

        if not generated_text:
            await message.edit_text(text=self.errors['TextGenerationFailed'])
            return ''

        await message.edit_text(text=self.finish_generation_message.format(generated_text=generated_text))
        return generated_text

    async def handle_audio_content(self, message: Message, generated_text: str) -> None:
        if self.audio_mode:
            generated_audio_path = await AudioContentGenerator().generate_content(generated_text)
            if not generated_audio_path:
                await message.edit_text(text=self.errors['AudioGenerationFailed'])
                return

            audio_file = FSInputFile(path=generated_audio_path, filename='Music.wav')
            await message.bot.send_audio(message.chat.id, audio=audio_file)

            # После отправки файл больше не нужен, значит можно удалить
            remove(generated_audio_path)

    async def execute(self, message: Message) -> None:
        await message.edit_text(text=self.start_generation_message)

        generated_text = await self.handle_text_content(message)
        if not generated_text:
            return

        await self.handle_audio_content(message, generated_text)
