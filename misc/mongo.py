from pymongo import MongoClient
from pymongo.server_api import ServerApi

import logging

logger = logging.getLogger(__name__)


def init(host: str, port: int) -> MongoClient:
    logger.info("init mongo connection")
    client = MongoClient(
        host,
        port
    )

    return client
