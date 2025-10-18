import json

from aiokafka import AIOKafkaProducer

from src.config import settings
from src.infrastructure.logger.impl import logger
from src.infrastructure.logger.interfaces import ILogger


class Producer:

    def __init__(self, settings, logger: ILogger):
        self.settings = settings
        self.logger = logger
        self.producer: AIOKafkaProducer | None = None

    async def start(self):
        if not self.producer:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.settings.KAFKA_HOSTS,
                enable_idempotence=True,
                acks='all',
                transactional_id='producer-tx-1',
                linger_ms=5,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=30000,
                retry_backoff_ms=1000
            )
            try:
                await self.producer.start()
                self.logger.info('Kafka producer started')
            except Exception:
                self.logger.error('Failed to start producer')
                raise

    async def send_message(self, message, partition: int | None = None):
        if not self.producer:
            await self.start()
        try:
            async with self.producer.transaction():
                self.logger.info(f'Begin transaction for message ID={message.id}')
                await self.producer.send_and_wait(
                    topic=self.settings.KAFKA_TOPIC,
                    value=message.model_dump(),
                    partition=partition
                )
                self.logger.info(f'Committed message ID={message.id}')

        except Exception:
            self.logger.error(f'Transaction failed for message {message.id}')
            try:
                await self.producer.abort_transaction()
                self.logger.warning(f'Aborted transaction for message {message.id}')
            except Exception:
                self.logger.error(f'Failed to abort transaction')
            raise


producer = Producer(settings, logger)
