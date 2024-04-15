import asyncio
from app import init
import logging

logging.basicConfig(level="DEBUG")


logger = logging.getLogger("__name__")



if __name__ == "__main__":
    asyncio.run(init())
