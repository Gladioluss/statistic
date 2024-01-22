import json

import loguru
from aio_pika.abc import AbstractIncomingMessage
from loguru import logger

from app import crud
from app.core.rabbit.messages_enums import EntityType
from app.database.session import SessionLocal
from app.schemas.defect_schema import IDefectCreate, IDefectUpdate


async def create_defect(message: AbstractIncomingMessage) -> None:

    """
    Create a defect from rabbit queued messages

    :param message: AbstractIncomingMessage
    :return: None
    """

    data = json.loads(message.body.decode('unicode_escape'))

    async with SessionLocal() as session:
        #TODO: Подумать над span и тд
        if message.headers["Name"] == EntityType.TOWER_DEFECTS:
            object_type = EntityType.TOWER_ENTITY
        loguru.logger.info(object_type)
        object = await crud.object.get_by_real_object_id_and_object_type(
            real_object_id=data["tower_id"],
            object_type=object_type,
            db_session=session,
        )
        new_defect = await crud.defect.create(
            obj_in=IDefectCreate(
                object_id=object.id,
                defect_id=data["id"],
                defect_description=data["description"]
            ),
            db_session=session,
        )
    logger.info(new_defect.id)


async def update_defect(message: AbstractIncomingMessage) -> None:

    """
    Update a defect from rabbit queued messages

    :param message: AbstractIncomingMessage
    :return: None
    """

    data = json.loads(message.body.decode('unicode_escape'))

    async with SessionLocal() as session:
        current_defect = await crud.defect.get_by_real_defect_id(
            real_defect_id=data["id"],
            db_session=session
        )
        subproject_updated = await crud.defect.update(
            obj_current=current_defect,
            obj_new=IDefectUpdate(
                name=data["name"],
                real_project_id=data["id"]
            ),
            db_session=session,
        )
    logger.info(subproject_updated)
