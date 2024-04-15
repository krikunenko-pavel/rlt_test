import os
import state
from aiogram import Bot, Dispatcher
from misc import mongo
from handlers import router

import logging

logger = logging.getLogger(__name__)


async def init():
    logger.info("init app")

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise Exception("Bot token is required")
    mongo_host = os.getenv("MONGO_HOST")
    mongo_port = int(os.getenv("MONGO_PORT", 27017))

    if not mongo_host:
        raise Exception("Mongo host is required")

    bot = Bot(token=token)

    bot.state = state.State(
        mongo_client=mongo.init(mongo_host, mongo_port)
    )

    dp = Dispatcher()
    dp.include_router(
        router
    )
    await dp.start_polling(
        bot,
        polling_timeout=5
    )
