from abc import ABC, abstractmethod

from aiogram.types import InlineKeyboardMarkup


class IKeyboard(ABC):
    @abstractmethod
    def get_keyboard(self) -> InlineKeyboardMarkup:
        pass
