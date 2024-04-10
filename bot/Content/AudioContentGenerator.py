from asyncio import sleep

from tts.main import TTS

from bot.Content import IContentGenerator


class AudioContentGenerator(IContentGenerator):
    async def generate_content(self, initial_text: str) -> str:
        return await TTS().generate_audio_by_text(initial_text)
