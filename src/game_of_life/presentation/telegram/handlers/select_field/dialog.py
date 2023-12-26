import logging
import operator
from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.kbd import Radio, Button, Group, Counter
from aiogram_dialog.widgets.text import Format, Const

from game_of_life.presentation.telegram.states.field import SelectFieldSG, FieldSG

SIZES = {
    1: (10, 10),
    2: (15, 15),
    3: (20, 20),
}


async def start(_message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SelectFieldSG.select_field, mode=StartMode.RESET_STACK)


async def handle_choice(call: CallbackQuery, _widget: Any, dialog_manager: DialogManager):
    radio = dialog_manager.find("r_sizes")
    counter = dialog_manager.find("evolve_counter")

    try:
        checked = int(radio.get_checked())
    except TypeError as _exc:
        await call.answer("Вы должны выбрать размер поля!")
        return

    width, height = SIZES[checked]
    evolves_per_tick = int(counter.get_value())

    await call.answer()
    await dialog_manager.start(FieldSG.field, data={
        "width": width,
        "height": height,
        "user_id": call.from_user.id,
        "evolve_per_tick": evolves_per_tick,
    })


async def get_sizes(**_kwargs):
    sizes = [
        ("10x10", 1),
        ("15x15", 2),
        ("20x20", 3),
    ]
    return {
        "sizes": sizes,
        "count": len(sizes),
    }


select_field_window = Window(
    Const('👋  Приветствую вас в моем боте, тут вы можете сыграть в игру "Жизнь" без смс и регистрации!\n'),
    Const("👇 Пожалуйста, выберите размер поля и кол-во эволюций в 3 секунды 👇"),
    Group(
        Radio(
            Format("🔘 {item[0]}"),
            Format("⚪️ {item[0]}"),
            id="r_sizes",
            item_id_getter=operator.itemgetter(1),
            items="sizes",
        ),
        width=1,
    ),
    Counter(
        id="evolve_counter",
        default=1,
        max_value=6,
    ),
    Button(Const("✅ Подтвердить"), id="select_size", on_click=handle_choice),
    state=SelectFieldSG.select_field,
    getter=get_sizes,
)

select_field_dialog = Dialog(select_field_window)
