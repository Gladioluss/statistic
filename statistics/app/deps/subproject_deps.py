import json
from uuid import UUID

from aio_pika.abc import AbstractIncomingMessage
from fastapi import Path
from loguru import logger
from typing_extensions import Annotated

from app import crud
from app.database.session import SessionLocal
from app.exceptions.common import IdNotFoundException
from app.models import Subproject
from app.schemas.subproject_schema import ISubprojectCreate, ISubprojectUpdate


async def create_subproject(message: AbstractIncomingMessage) -> None:
    """
    Create a subproject from rabbit queued messages

    :param message: AbstractIncomingMessage
    :return: None
    """

    data = json.loads(message.body.decode('unicode_escape'))

    async with SessionLocal() as session:
        project_id = await crud.project.get_project_id_by_real_project_id(
            real_project_id=data['project_id'],
            db_session=session,
        )
        new_subproject = await crud.subproject.create(
            obj_in=ISubprojectCreate(
                name=data["name"],
                project_id=project_id,
                real_subproject_id=data["id"]
            ),
            db_session=session,
        )
    logger.info(new_subproject)


async def update_subproject(message: AbstractIncomingMessage) -> None:
    """
    Update a subproject from rabbit queued messages

    :param message: AbstractIncomingMessage
    :return: None
    """

    data = json.loads(message.body.decode('unicode_escape'))

    async with SessionLocal() as session:
        current_subproject = await crud.subproject.get_by_real_subproject_id(
            real_subproject_id=data["id"],
            db_session=session
        )
        subproject_updated = await crud.subproject.update(
            obj_current=current_subproject,
            obj_new=ISubprojectUpdate(
                name=data["name"],
                real_project_id=data["id"]
            ),
            db_session=session,
        )
    logger.info(subproject_updated)


async def get_subproject_by_id_from_path(
        id: Annotated[UUID, Path(description="The UUID id of the project")]
) -> Subproject:
    """
    Get a subproject from the database by id from the path

    :param id: UUID
    :return: Subproject
    """

    project = await crud.project.get(id=id)
    if not project:
        raise IdNotFoundException(Subproject, incoming_id=id)
    return project
