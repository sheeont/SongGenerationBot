import asyncio
import logging

from models import yandex_llm as gen

from bot.Content import IContentGenerator
from bot.config import text_model_temperature
from bot.Utils import Utils


class TextContentGenerator(IContentGenerator):
    async def generate_content(self, initial_text: str, style_type: str) -> str:
        task = f"Первая строка: {initial_text}\nЖанр: {style_type}"

        try:
            timeout_seconds = 60
            generated_text: str = await asyncio.wait_for(
                gen.generate_song(task, text_model_temperature / 10),
                timeout_seconds
            )
            generated_text = Utils.replace_bold(generated_text)
            return generated_text
        except asyncio.TimeoutError:
            logging.error("TimeoutError: Превышено время ожидания генерации текста.")
        except Exception as error:
            logging.error(error)

        return ""
