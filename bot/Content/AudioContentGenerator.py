import logging

from tts.suno_songs import generate_audio

from bot.Content import IContentGenerator


class AudioContentGenerator(IContentGenerator):
    async def generate_content(self, initial_text: str, style_type: str) -> str:
        # return await TTS().generate_audio_by_text(initial_text)

        try:
            return await generate_audio(initial_text, style_type, True)
        except Exception as error:
            logging.error(error)

        return ""
