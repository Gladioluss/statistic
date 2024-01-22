from dataclasses import dataclass

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustChannel, AbstractRobustConnection
from loguru import logger

from app.core.rabbit.messages_enums import ActionType, EntityType
from app.core.rabbit.rabbit_settings import rmq_settings
from app.deps.defects_deps import create_defect, update_defect
from app.deps.object_deps import create_object, update_object
from app.deps.progress_deps import new_progress
from app.deps.project_deps import create_project, update_project
from app.deps.subproject_deps import create_subproject, update_subproject


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
            self.connection = await connect_robust(rmq_settings.basic.rabbit_url)
            self.channel = await self.connection.channel(publisher_confirms=False)

            logger.info('Successfully connected to the RabbitMQ!')

            await self.declare_queue()
            await self.consume_queue()

        except Exception as e:
            await self._clear()
            logger.error(e)

    async def declare_queue(self) -> None:

        """
        Declare queue

        :return: None

        """
        await self.channel.set_qos(prefetch_count=1)
        await self.channel.declare_queue(
            name=rmq_settings.projects.queue,
            auto_delete=rmq_settings.projects.auto_delete,
            durable=rmq_settings.projects.durable
        )
        logger.info('Declared queue "{}"', rmq_settings.projects.queue)

        await self.channel.declare_queue(
            name=rmq_settings.defects.queue,
            auto_delete=rmq_settings.defects.auto_delete,
            durable=rmq_settings.defects.durable
        )
        logger.info('Declared queue "{}"', rmq_settings.defects.queue)

    async def consume_queue(self) -> None:

        """
        Get queues

        :return: None
        """

        receive_queue_projects = await self.channel.get_queue(rmq_settings.projects.queue)
        await receive_queue_projects.consume(self.receive_processing_projects)
        receive_queue_defects = await self.channel.get_queue(rmq_settings.defects.queue)
        await receive_queue_defects.consume(self.receive_processing_defects)

    async def receive_processing_projects(self, message: AbstractIncomingMessage) -> None:

        """
        Get project from message

        :param message: AbstractIncomingMessage
        :return: None
        """

        entity_type = EntityType(message.headers["Name"])
        action_type = ActionType(message.headers["Type"])


        if entity_type == EntityType.PROJECT:
            if action_type == ActionType.CREATE:
                await create_project(message)
            elif action_type == ActionType.UPDATE:
                await update_project(message)

        elif entity_type == EntityType.SUBPROJECT:
            if action_type == ActionType.CREATE:
                await create_subproject(message)
            elif action_type == ActionType.UPDATE:
                await update_subproject(message)

        elif (entity_type == EntityType.TOWER_ENTITY or
              entity_type == EntityType.SPAN_ENTITY):
            if action_type == ActionType.CREATE:
                object_id = await create_object(message)
                await new_progress(object_id, message)
            elif action_type == ActionType.UPDATE:
                object_id = await update_object(message)
                await new_progress(object_id, message)

        await message.ack()

    async def receive_processing_defects(self, message: AbstractIncomingMessage) -> None:

        """
        Get defect from message

        :param message: AbstractIncomingMessage
        :return: None

        """
        entity_type = EntityType(message.headers["Name"])
        action_type = ActionType(message.headers["Type"])

        if entity_type == EntityType.TOWER_DEFECTS:
            if action_type == ActionType.CREATE:
                await create_defect(message)
            elif action_type == ActionType.UPDATE:
                await update_defect(message)

        await message.ack()

    async def disconnect(self) -> None:

        """
        Disconnect and clear connections from RabbitMQ

        :return: None
        """

        await self._clear()



rabbit_connection = RabbitConnection()
