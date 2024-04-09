from Content import IContentGenerator
from main import tts_instance


class AudioContentGenerator(IContentGenerator):
    async def generate_content(self, initial_text: str) -> str:
        return tts_instance.generate_audio_by_text(initial_text)
