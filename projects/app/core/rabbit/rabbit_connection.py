import json
from dataclasses import dataclass

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from loguru import logger

from app.core.config import settings


@dataclass
class RabbitConnection:
    connection: AbstractRobustConnection | None = None
    channel: AbstractRobustChannel | None = None

    def status(self) -> bool:
        """
            Checks if connection established

            :return: True if connection established
        """
        if self.connection.is_closed or self.channel.is_closed:
            return False
        return True

    async def _clear(self) -> None:
        if not self.channel.is_closed:
            await self.channel.close()
        if not self.connection.is_closed:
            await self.connection.close()

        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        """
        Establish connection with the RabbitMQ

        :return: None
        """
        logger.info('Connecting to the RabbitMQ...')
        try:
            self.connection = await connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel(publisher_confirms=False)
            logger.info('Successfully connected to the RabbitMQ!')
        except Exception as e:
            await self._clear()
            logger.error(e.dict)

    async def disconnect(self) -> None:
        """
        Disconnect and clear connections from RabbitMQ

        :return: None
        """
        await self._clear()

    async def send_messages(
            self,
            headers: dict,
            messages: dict,
            routing_key: str = settings.QUEUE_NAME
    ) -> None:
        """
            Public message or messages to the RabbitMQ queue.

            :param headers: dict of headers to send.
            :param messages: dict with messages objects.
            :param routing_key: Routing key of RabbitMQ, not required. Tip: the same as in the consumer.
        """
        if not self.channel:
            raise RuntimeError('The message could not be sent because the connection with RabbitMQ is not established')

        async with self.channel.transaction():
            messages = Message(
                headers=headers,
                body=json.dumps(messages).encode()
            )

            await self.channel.default_exchange.publish(
                messages, routing_key=routing_key,
            )


rabbit_connection = RabbitConnection()
