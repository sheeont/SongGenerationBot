from os import getenv
from typing import Any, Union, Dict

from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.config import is_development_now


class IsDevelopmentFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        return is_development_now and (not message.from_user.username or (message.from_user.username not in getenv('ADMIN_USERNAMES')))
