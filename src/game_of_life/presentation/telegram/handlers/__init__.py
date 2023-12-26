from aiogram import Dispatcher
from aiogram.filters import Command

from .field.dialog import field_dialog
from .select_field.dialog import start, select_field_dialog


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(start, Command(commands="start"))


def register_dialogs(dp: Dispatcher) -> None:
    dp.include_router(field_dialog)
    dp.include_router(select_field_dialog)


__all__ = [
    "register_handlers",
    "register_dialogs",
]
