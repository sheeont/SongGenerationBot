from abc import ABC, abstractmethod


class IContentGenerator:
    # TODO: Доделать
    @abstractmethod
    def generate_content(self, initial_text: str):
        pass
