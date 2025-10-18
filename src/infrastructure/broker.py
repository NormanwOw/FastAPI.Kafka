import asyncio

from aiokafka.errors import KafkaConnectionError
from faststream.kafka import KafkaBroker

from src.config import KAFKA_URL, settings, Settings
from src.infrastructure.logger.impl import logger
from src.infrastructure.logger.interfaces import ILogger


class MyKafkaBroker(KafkaBroker):

    def __init__(self, url: str, settings: Settings, logger: ILogger):
        super().__init__(url)
        self.settings = settings
        self.logger = logger
        self.new_publisher = self.publisher(self.settings.KAFKA_TOPIC)

    async def try_to_connect(self, try_counter: int = 1):
        try:
            await self.connect()
        except KafkaConnectionError:
            if try_counter > 5:
                self.logger.error('Failed to connect to Kafka broker after 5 tries')
                raise
            await asyncio.sleep(5)
            await self.try_to_connect(try_counter + 1)

    async def get_publisher(self):
        return self.new_publisher


broker = MyKafkaBroker(KAFKA_URL, settings, logger)
