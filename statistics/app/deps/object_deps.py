import json
from uuid import UUID

from aio_pika.abc import AbstractIncomingMessage
from fastapi import Path
from loguru import logger
from typing_extensions import Annotated

from app import crud
from app.database.session import SessionLocal
from app.exceptions.common import IdNotFoundException
from app.models import Object
from app.schemas.object_schema import IObjectCreate, IObjectUpdate


async def create_object(message: AbstractIncomingMessage) -> UUID:

    """
    Create an object from rabbit queued messages

    :param message: AbstractIncomingMessage
    :return: None
    """

    data = json.loads(message.body.decode('unicode_escape'))

    async with SessionLocal() as session:
        subproject_id = await crud.subproject.get_subproject_id_by_real_subproject_id(
            real_subproject_id=data['subproject_id'],
            db_session=session,
        )
        new_object = await crud.object.create(
            obj_in=IObjectCreate(
                object_type=message.headers["Name"],
                real_object_id=data["id"],
                subproject_id=subproject_id,
                status=message.headers["Status"],
            ),
            db_session=session,
        )

    logger.info(data)
    return new_object.id


async def update_object(message: AbstractIncomingMessage) -> UUID:

    """
    Update an object from rabbit queued messages

    :param message: AbstractIncomingMessage
    :return: None
    """

    data = json.loads(message.body.decode('unicode_escape'))

    async with SessionLocal() as session:
        current_object = await crud.object.get_by_real_object_id_and_object_type(
            real_object_id=data["id"],
            object_type=message.headers["Name"],
            db_session=session
        )
        project_updated = await crud.object.update(
            obj_current=current_object,
            obj_new=IObjectUpdate(
                name=data["name"],
                real_object_id=data["id"],
                status=message.headers["Status"]
            ),
            db_session=session,
        )
    logger.info(f"Update {message.headers['Name']}")
    return project_updated.id


async def get_object_by_id_from_path(
        object_id: Annotated[UUID, Path(description="The UUID id of the object")]
) -> Object:

    """
    Get object from database by id from path

    :param object_id: UUID
    :return: Object
    """

    project = await crud.object.get(id=object_id)
    if not project:
        raise IdNotFoundException(Object, incoming_id=object_id)
    return project
