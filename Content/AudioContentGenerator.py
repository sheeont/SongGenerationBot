from asyncio import sleep

from Content import IContentGenerator


class AudioContentGenerator(IContentGenerator):
    async def generate_content(self, initial_text: str) -> str:
        # Заглушка
        await sleep(2)
        generated_audio_path = './AudioFiles/test_audio.wav'
        return generated_audio_path
