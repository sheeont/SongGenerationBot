import asyncio
import logging

from models import yandex_llm as gen

from bot.Content import IContentGenerator
from bot.config import text_model_temperature


class TextContentGenerator(IContentGenerator):
    def __init__(self, style_type, initial_text):
        self.style_type = style_type
        self.initial_text = initial_text

    async def generate_content(self, initial_text: str) -> str:
        task = f"Первая строка: {self.initial_text}\nЖанр: {self.style_type}"
        try:
            timeout_seconds = 60
            generated_text = await asyncio.wait_for(gen.generate_song(task, text_model_temperature), timeout_seconds)
            return generated_text
        except asyncio.TimeoutError:
            logging.error("TimeoutError: Превышено время ожидания генерации текста.")
        except Exception as error:
            logging.error(error)

        return ""
