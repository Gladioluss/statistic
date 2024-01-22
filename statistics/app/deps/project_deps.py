import json
from datetime import date
from uuid import UUID

from aio_pika.abc import AbstractIncomingMessage
from fastapi import Path, Query
from loguru import logger
from typing_extensions import Annotated

from app import crud
from app.database.session import SessionLocal
from app.exceptions.common import IdNotFoundException
from app.models import Project
from app.models.objects import ObjectStatus
from app.schemas.project_schema import IProjectCreate, IProjectUpdate


async def create_project(message: AbstractIncomingMessage) -> None:

    """
    Create a project from rabbit queued messages

    :param message: AbstractIncomingMessage
    :return: None
    """

    data = json.loads(message.body.decode('unicode_escape'))

    async with SessionLocal() as session:
        new_project = await crud.project.create(
            obj_in=IProjectCreate(
                name=data["name"],
                real_project_id=data["id"]
            ),
            db_session=session,
        )
    logger.info(new_project)


async def update_project(message: AbstractIncomingMessage) -> None:

    """
    Update a project from rabbit queued messages

    :param message: AbstractIncomingMessage
    :return: None
    """

    data = json.loads(message.body.decode('unicode_escape'))

    async with SessionLocal() as session:
        current_project = await crud.project.get_by_real_project_id(
            real_project_id=data["id"],
            db_session=session
        )
        project_updated = await crud.project.update(
            obj_current=current_project,
            obj_new=IProjectUpdate(
                name=data["name"],
                real_project_id=data["id"]
            ),
            db_session=session,
        )
    logger.info(project_updated)


async def get_project_by_id_from_path(
        project_id: Annotated[UUID, Path(description="The UUID id of the project")]
) -> Project:

    """
    Get project from database by id from path

    :param project_id: UUID
    :return: Project
    """
    project = await crud.project.get(id=project_id)
    if not project:
        raise IdNotFoundException(Project, incoming_id=project_id)
    return project


async def get_project_by_date_from_path(
        project_id: Annotated[UUID, Path(description="The UUID id of the project")],
        selected_date: Annotated[date, Path(description="The date of the project")],
) -> Project:

    """
    Get a project from the database by id
    before the received date from the path

    :param project_id: UUID
    :param selected_date: date
    :return: Project
    """

    project = await crud.project.get(id=project_id)

    if not project:
        raise IdNotFoundException(Project, incoming_id=project_id)

    subprojects = []
    for subproject in project.subprojects:

        objects = []
        for object in subproject.objects:
            progresses = []
            status: str = ObjectStatus.NOT_READY
            logger.error(len(object.progresses))
            for progress in object.progresses:

                progress_date = date(progress.time.year, progress.time.month, progress.time.day_of_month)
                if selected_date >= progress_date:

                    progresses.append(progress)
                    if progress.progress is True:
                        status = ObjectStatus.READY
                        # break

            object.progresses = progresses
            object.status = status

            if len(object.progresses) != 0:
                objects.append(object)

        subproject.objects = objects
        subprojects.append(subproject)
    project.subprojects = subprojects

    return project


async def get_project_by_year_from_path(
        project_id: Annotated[UUID, Path(description="The UUID id of the project")],
        year: Annotated[int, Path(description="The year of the project")],
) -> Project:

    """
    Get a project from the database by id
    before the received year from the path

    :param project_id: UUID
    :param year: int
    :return: Project
    """

    project = await crud.project.get(id=project_id)

    if not project:
        raise IdNotFoundException(Project, incoming_id=project_id)

    subprojects = []
    for subproject in project.subprojects:

        objects = []
        for object in subproject.objects:

            progresses = []
            status: str = ObjectStatus.READY
            for progress in object.progresses:

                if year == progress.time.year:

                    progresses.append(progress)
                    if progress.progress is False:
                        status = ObjectStatus.NOT_READY
                    else:
                        status = ObjectStatus.READY
                        break

            object.progresses = progresses
            object.status = status
            if len(object.progresses) != 0:
                objects.append(object)
        subproject.objects = objects
        subprojects.append(subproject)
    project.subprojects = subprojects

    return project


async def get_project_by_quarter(
        project_id: Annotated[UUID, Path(description="The UUID id of the project")],
        year: Annotated[int, Query(description="The year of the project")],
        quarter: Annotated[int, Query(description="The quarter of the project")],
) -> Project:

    """
    Get a project from the database by id
    before the received quarter from the path

    :param project_id: UUID,
    :param year: int,
    :param quarter: int
    :return: Project
    """

    project = await crud.project.get(id=project_id)

    if not project:
        raise IdNotFoundException(Project, incoming_id=project_id)

    subprojects = []
    for subproject in project.subprojects:

        objects = []
        for object in subproject.objects:

            progresses = []
            status: str = ObjectStatus.READY
            for progress in object.progresses:

                if (year == progress.time.year and quarter <= progress.time.quarter) or year < progress.time.year:

                    progresses.append(progress)
                    if progress.progress is False:
                        status = ObjectStatus.NOT_READY
                    else:
                        status = ObjectStatus.READY
                        break

            object.progresses = progresses
            object.status = status
            if len(object.progresses) != 0:
                objects.append(object)
        subproject.objects = objects
        subprojects.append(subproject)
    project.subprojects = subprojects

    return project
