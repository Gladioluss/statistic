import json

from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params
from uuid import UUID
from typing import Annotated

from loguru import logger

from app import crud
from app.core.rabbit.queue_message_settings import QueueHeaders, QueueHeaderTypeValues
from app.core.rabbit.rabbit_connection import rabbit_connection

from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    IDeleteResponseBase,
    create_response,
)

from app.schemas.project_schema import (
    IProjectWithStatus,
    IFullProjectInfoRead,
    IProjectRead,
    IProjectCreate,
    IProjectUpdate,
    IProjectWithSubprojectsListRead,
)

from app.models.project import Project
from app.models.status import ProjectStatus
from app.deps import project_deps, project_status_deps
from app.utils.checks import project_checks, project_status_checks

router = APIRouter()


@router.get("/list")
async def get_projects(
        params: Params = Depends()
) -> IGetResponsePaginated[IProjectRead]:
    """
    Gets a paginated list of projects
    """
    projects = await crud.project.get_multi_paginated(params=params)
    return create_response(data=projects)


@router.get("/list/id")
async def get_projects_id(
) -> IGetResponseBase[list[UUID]]:
    """
    Gets a list of projects id
    """
    projects = await crud.project.get_all_id()
    return create_response(data=projects)


@router.get("/list/status")
async def get_projects_list_by_project_status_id(
        current_project_status: ProjectStatus = Depends(project_status_deps.get_project_status_by_id_from_query),
        params: Params = Depends()
) -> IGetResponsePaginated[IProjectRead]:
    """
    Gets a paginated list of projects by status id
    """
    projects = await crud.project.get_paginated_list_by_status_id(
        status_id=current_project_status.id,
        params=params
    )

    return create_response(data=projects)


@router.get("/{id}")
async def read_project_by_id(
        project: Project = Depends(project_deps.get_project_by_id_from_path)
) -> IGetResponseBase[IProjectRead]:
    """
    Gets a project by id
    """
    return create_response(data=project)


@router.get("/{id}/subprojects")
async def get_project_with_subprojects_list_by_id(
        project: Project = Depends(project_deps.get_project_by_id_from_path)
) -> IGetResponseBase[IProjectWithSubprojectsListRead]:
    """
    Gets a project by id
    """
    return create_response(data=project)


@router.get("/{id}/status")
async def get_project_with_status_by_id(
        project: Project = Depends(project_deps.get_project_by_id_from_path)
) -> IGetResponseBase[IProjectWithStatus]:
    """
    Gets a project by id
    """
    return create_response(data=project)


@router.get("/{id}/full")
async def get_full_project_info_by_id(
        project: Project = Depends(project_deps.get_project_by_id_from_path)
) -> IGetResponseBase[IFullProjectInfoRead]:
    """
    Gets a full project information by id
    """
    return create_response(data=project)


@router.post("")
async def create_project(
        project: IProjectCreate
) -> IPostResponseBase[IProjectRead]:
    """
    Creates a new project
    """
    await project_checks.project_name_is_taken(name=project.name)
    if project.status_id: #todo потому что необяз поле
        await project_status_checks.project_status_is_exist(id=project.status_id)
    new_project = await crud.project.create(obj_in=project)
    await rabbit_connection.send_messages(
        headers={
            QueueHeaders.NAME: new_project.__tablename__,
            QueueHeaders.TYPE: QueueHeaderTypeValues.CREATE
        },
        messages=new_project.to_dict()
    )
    return create_response(data=new_project)


@router.put("/{id}")
async def update_project(
    project: IProjectUpdate,
    current_project: Project = Depends(project_deps.get_project_by_id_from_path)
) -> IPutResponseBase[IProjectRead]:
    """
    Updates a project by its id
    """
    if project.name:
        await project_checks.project_name_is_taken(name=project.name)
    if project.status_id:
        await project_status_checks.project_status_is_exist(id=project.status_id)

    project_updated = await crud.project.update(obj_current=current_project, obj_new=project)
    await rabbit_connection.send_messages(
        headers={
            QueueHeaders.NAME: project_updated.__tablename__,
            QueueHeaders.TYPE: QueueHeaderTypeValues.UPDATE
        },
        messages=project_updated.to_dict()
    )
    return create_response(data=project_updated)

@router.delete("/{id}")
async def delete_project(
        current_project: Project = Depends(project_deps.get_project_by_id_from_path)
) -> IDeleteResponseBase[IProjectRead]:
    """
    Deletes a project by its id
    """
    project_deleted = await crud.project.remove(id=current_project.id)
    return create_response(data=project_deleted)



