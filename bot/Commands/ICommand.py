from abc import ABC, abstractmethod

from aiogram.types import Message


class ICommand(ABC):
    @abstractmethod
    async def execute(self, message: Message) -> None:
        pass
