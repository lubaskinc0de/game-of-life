import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder, RedisEventIsolation

from aiogram_dialog import setup_dialogs

from game_of_life.presentation.telegram.field_manager import FieldManager
from game_of_life.presentation.telegram.field_manager_middleware import FieldManagerMiddleware
from game_of_life.presentation.telegram.handlers import register_handlers, register_dialogs


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    token = os.environ.get("BOT_TOKEN")
    bot = Bot(token=token, parse_mode="html")

    storage: RedisStorage = RedisStorage.from_url(
        "redis://bot_redis:6379", key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    dp = Dispatcher(
        events_isolation=RedisEventIsolation(redis=storage.redis),
        storage=storage,
    )

    manager = FieldManager()
    middleware = FieldManagerMiddleware(field_manager=manager)

    dp.message.outer_middleware(middleware)
    dp.callback_query.outer_middleware(middleware)
    dp.update.outer_middleware(middleware)

    register_handlers(dp)
    register_dialogs(dp)

    setup_dialogs(dp)

    try:
        await dp.start_polling(bot)
    finally:
        logging.info("Shutdown..")


if __name__ == "__main__":
    asyncio.run(main())
