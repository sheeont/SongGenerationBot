from abc import ABC, abstractmethod


class IContentGenerator(ABC):
    @abstractmethod
    async def generate_content(self, initial_text: str, style_type: str) -> str:
        pass
