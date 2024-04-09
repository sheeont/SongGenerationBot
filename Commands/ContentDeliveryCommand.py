from os import remove
from os.path import exists

from aiogram.types import Message, FSInputFile

from Commands import ICommand
from Content import TextContentGenerator, AudioContentGenerator


class ContentDeliveryCommand(ICommand):
    errors = {
        'TextGenerationFailed': 'Произошла ошибка при генерации текста',
        'AudioGenerationFailed': 'Произошла ошибка при генерации аудио'
    }

    text = ('Сгенерированный текст:\n\n'
            '{generated_text}')

    def __init__(self, audio_mode: bool):
        self.audio_mode = audio_mode

    async def execute(self, message: Message) -> None:
        generated_text = await TextContentGenerator().generate_content(message.text)

        if not generated_text:
            await message.answer(text=self.errors['TextGenerationFailed'])
            return

        await message.answer(text=self.text.format(generated_text=generated_text))

        if self.audio_mode:
            generated_audio_path = await AudioContentGenerator().generate_content(generated_text)
            if not generated_audio_path:
                await message.answer(text=self.errors['AudioGenerationFailed'])
                return

            audio_file = FSInputFile(path=generated_audio_path, filename='Music.wav')
            await message.bot.send_audio(message.chat.id, audio=audio_file)

            # После отправки файл больше не нужен, значит можно удалить
            remove(generated_audio_path)
