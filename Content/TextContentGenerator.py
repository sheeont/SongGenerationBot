from asyncio import sleep

from Content import IContentGenerator


class TextContentGenerator(IContentGenerator):
    async def generate_content(self, initial_text: str) -> str:
        # Заглушка
        await sleep(2)
        generated_text = 'Сгенерированный текст'
        return generated_text
