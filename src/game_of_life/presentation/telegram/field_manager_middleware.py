from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from game_of_life.presentation.telegram.field_manager import FieldManager


class FieldManagerMiddleware(BaseMiddleware):
    def __init__(self, field_manager: FieldManager) -> None:
        self.field_manager = field_manager

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        data["field_manager"] = self.field_manager
        result = await handler(event, data)
        return result
