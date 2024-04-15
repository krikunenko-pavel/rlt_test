from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)


class State:
    def __init__(self, mongo_client: MongoClient):
        logger.info("init app state")
        self.mongo_client: MongoClient = mongo_client
        self.mongo_db = mongo_client['sampleDB']
        self.mongo_collection = self.mongo_db['sample_collection']