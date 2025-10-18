from src.config import Settings, settings
from src.domain.entites import Message
from src.infrastructure.broker import MyKafkaBroker, broker
from src.infrastructure.logger.impl import logger
from src.infrastructure.logger.interfaces import ILogger


class Consumer:

    def __init__(self, broker: MyKafkaBroker, settings: Settings, logger: ILogger):
        self.broker = broker
        self.subscriber = broker.subscriber(
            settings.KAFKA_TOPIC,
            group_id=settings.KAFKA_GROUP,
            auto_offset_reset='earliest'
        )
        self.logger = logger

    async def start(self):
        await self.broker.try_to_connect()
        await self.subscriber.start()
        async for message in self.subscriber:
            try:
                data: str = message.body.decode('utf-8')
                msg = Message.model_validate_json(data)
                self.logger.info(f'Received: {msg}')
                await message.ack()
            except Exception:
                self.logger.error(f'Error processing message {message}')
                await message.nack()


consumer = Consumer(broker, settings, logger)