from asyncio import sleep

from Content import IContentGenerator


class TextContentGenerator(IContentGenerator):
    def __init__(self, style_type, initial_text):
        self.style_type = style_type
        self.initial_text = initial_text

    async def generate_content(self, initial_text: str) -> str:
        # Заглушка
        await sleep(2)
        generated_text = f'{self.style_type}\n{self.initial_text}'
        return generated_text
