from src.domain.entites import Message
from src.infrastructure.broker import MyKafkaBroker
from src.infrastructure.logger.interfaces import ILogger


class Producer:

    def __init__(self, broker: MyKafkaBroker, logger: ILogger):
        self.broker = broker
        self.logger = logger

    async def send_message(self, message: Message, partition: int = None):
        await self.broker.try_to_connect()
        await self.broker.new_publisher.publish(message.model_dump(), partition=partition)
        self.logger.info(f'Send message with ID {message.id}')
