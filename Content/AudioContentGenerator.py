from asyncio import sleep

from Content import IContentGenerator


class AudioContentGenerator(IContentGenerator):
    # Функция заглушка. Просто для разработки
    @staticmethod
    def create_file():
        with open('./FilesForDevelopment/test_audio.wav', 'rb') as file:
            data = file.read()

        with open('./AudioFiles/test_audio.wav', 'wb') as file:
            file.write(data)

    async def generate_content(self, initial_text: str) -> str:
        # Заглушка
        await sleep(2)
        self.create_file()
        generated_audio_path = './AudioFiles/test_audio.wav'
        return generated_audio_path
