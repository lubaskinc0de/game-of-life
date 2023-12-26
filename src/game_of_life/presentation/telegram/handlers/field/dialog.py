import asyncio
import logging
from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from game_of_life.domain.entities.field import Field
from game_of_life.domain.services.field import FieldService
from game_of_life.domain.value_objects.node_position import NodePosition
from game_of_life.presentation.telegram.field_manager import FieldManager
from game_of_life.presentation.telegram.states.field import FieldSG

IS_RUNNING = "is_running"
DELAY = 3.2
MAX_ITERATIONS = 20


def render_field(width: int, height: int, field: Field) -> str:
    field_render = ""

    for y in range(0, height):
        for x in range(0, width):
            position = NodePosition((x, y))
            node = field.get_node(position)

            if not node:
                field_render += "⬜"
            else:
                field_render += "⬛"
        field_render += "\n"

    return field_render


def create_field(width: int, height: int, user_id: int, field_manager: FieldManager) -> Field:
    field_service = FieldService()
    field = field_service.random(width, height)

    field_manager.set(user_id, field)

    return field


async def get_rendered_field(dialog_manager: DialogManager, **_kwargs):
    width, height = dialog_manager.start_data["width"], dialog_manager.start_data["height"]

    field_manager: FieldManager = dialog_manager.middleware_data["field_manager"]
    user_id = dialog_manager.start_data["user_id"]

    try:
        field = field_manager.get(user_id)
    except KeyError:
        logging.warning("No field for user id %d", user_id)
        field = create_field(width, height, user_id, field_manager)

    field_render = render_field(width, height, field)

    return {
        "field": field_render,
        IS_RUNNING: field_manager.is_running(user_id)
    }


async def evolve_process(
        field: Field,
        bg: DialogManager,
        field_manager: FieldManager,
        user_id: int,
        width: int,
        height: int,
        evolve_per_tick: int,
) -> None:
    counter = 0

    while field.is_anyone_alive and field_manager.is_running(user_id):
        await bg.update({
            "field": render_field(
                width=width,
                height=height,
                field=field,
            ),
            IS_RUNNING: field_manager.is_running(user_id),
        })

        for x in range(evolve_per_tick):
            field.next_generation()

        await asyncio.sleep(DELAY)

        counter += 1
        if counter > MAX_ITERATIONS:
            try:
                field_manager.stop(user_id)

                break
            except KeyError:
                break
            finally:
                await bg.update({
                    IS_RUNNING: False,
                })


async def start_evolve(call: CallbackQuery, _widget: Any, dialog_manager: DialogManager):
    field_manager: FieldManager = dialog_manager.middleware_data["field_manager"]
    user_id = dialog_manager.start_data["user_id"]
    width, height = dialog_manager.start_data["width"], dialog_manager.start_data["height"]

    await call.answer()

    try:
        field = field_manager.get(user_id)
    except KeyError:
        logging.warning("No field for user id %d", user_id)
        field = create_field(width, height, user_id, field_manager)

    field_manager.run(user_id)

    asyncio.create_task(evolve_process(
        field,
        dialog_manager.bg(),
        field_manager,
        user_id,
        dialog_manager.start_data["width"],
        dialog_manager.start_data["height"],
        dialog_manager.start_data["evolve_per_tick"],
    ))


async def stop_evolve(call: CallbackQuery, _widget: Any, dialog_manager: DialogManager):
    field_manager: FieldManager = dialog_manager.middleware_data["field_manager"]
    user_id = dialog_manager.start_data["user_id"]

    try:
        field_manager.stop(user_id)
    except KeyError:
        await to_main_menu(call, _widget, dialog_manager)

    await call.answer()


async def regenerate_field(call: CallbackQuery, _widget: Any, dialog_manager: DialogManager):
    field_manager: FieldManager = dialog_manager.middleware_data["field_manager"]
    user_id = dialog_manager.start_data["user_id"]
    width, height = dialog_manager.start_data["width"], dialog_manager.start_data["height"]

    try:
        field_manager.stop(user_id)
    except KeyError:
        pass

    create_field(width, height, user_id, field_manager)

    await call.answer()


async def next_generation(call: CallbackQuery, _widget: Any, dialog_manager: DialogManager):
    field_manager: FieldManager = dialog_manager.middleware_data["field_manager"]
    user_id = dialog_manager.start_data["user_id"]

    await call.answer()

    try:
        field = field_manager.get(user_id)
    except KeyError:
        await to_main_menu(call, _widget, dialog_manager)
    else:
        field.next_generation()


async def to_main_menu(call: CallbackQuery, _widget: Any, dialog_manager: DialogManager):
    field_manager: FieldManager = dialog_manager.middleware_data["field_manager"]
    user_id = dialog_manager.start_data["user_id"]

    try:
        field_manager.stop(user_id)
    except KeyError:
        pass
    else:
        field_manager.remove(user_id)
    finally:
        await call.answer()
        await dialog_manager.done()


field_window = Window(
    Format("{field}"),
    Button(Const("🚀 Начать цикл"), id="start_evolution", on_click=start_evolve, when=F[IS_RUNNING].is_not(True)),
    Button(Const("⛔ Остановить цикл"), id="stop_evolution", on_click=stop_evolve, when=F[IS_RUNNING]),
    Button(Const("▶️ Сделать ход"), id="next_generation", on_click=next_generation, when=F[IS_RUNNING].is_not(True)),
    Button(Const("🔄 Регенерировать"), id="regenerate", on_click=regenerate_field),
    Button(Const("👈 Назад"), id="to_main_menu", on_click=to_main_menu),
    state=FieldSG.field,
    getter=get_rendered_field,
)

field_dialog = Dialog(field_window)
