from aiogram.filters.state import StatesGroup, State


class SelectFieldSG(StatesGroup):
    select_field = State()


class FieldSG(StatesGroup):
    field = State()
