from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params
from uuid import UUID
from typing import Annotated

from app.deps import project_status_deps
from app.utils.checks import project_status_checks
from app import crud
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    IDeleteResponseBase,
    create_response,
)
from app.schemas.project_status_schema import (
    IProjectStatusWithProjectsRead,
    IProjectStatusRead,
    IProjectStatusCreate,
    IProjectStatusUpdate,
    IProjectStatusWithSubrojectsRead,
    IProjectStatusWithSubrojectsAndProjectsRead
)
from app.utils.exceptions.common import IdNotFoundException, NameNotFoundException, NameExistException
from app.models.status import ProjectStatus

router = APIRouter()


@router.get("")
async def get_project_statuses(
        params: Params = Depends()
) -> IGetResponsePaginated[IProjectStatusRead]:
    """
    Gets a paginated list of project statuses
    """
    project_statuses = await crud.project_status.get_multi_paginated(params=params)
    return create_response(data=project_statuses)


@router.get("/{id}")
async def read_project_status_by_id(
        project_status: ProjectStatus = Depends(project_status_deps.get_project_status_by_id_from_path)
) -> IGetResponseBase[IProjectStatusRead]:
    """
    Gets a project status by id
    """
    return create_response(data=project_status)


@router.get("/{id}/projects")
async def get_project_status_with_projects_list_by_id(
        project_status: ProjectStatus = Depends(project_status_deps.get_project_status_by_id_from_path)
) -> IGetResponseBase[IProjectStatusWithProjectsRead]:
    """
    Gets a project status with projects list by id
    """
    return create_response(data=project_status)


@router.get("/{id}/subprojects")
async def get_project_status_with_subprojects_list_by_id(
        project_status: ProjectStatus = Depends(project_status_deps.get_project_status_by_id_from_path)
) -> IGetResponseBase[IProjectStatusWithSubrojectsRead]:
    """
    Gets a project status with subprojects list by id
    """
    return create_response(data=project_status)


@router.get("/{id}/full")
async def get_project_status_with_subprojects_and_projects_list_by_id(
        project_status: ProjectStatus = Depends(project_status_deps.get_project_status_by_id_from_path)
) -> IGetResponseBase[IProjectStatusWithSubrojectsAndProjectsRead]:
    """
    Gets a project status with subprojects and projects list by id
    """
    return create_response(data=project_status)


@router.post("")
async def create_project_status(
        project_status: IProjectStatusCreate
) -> IPostResponseBase[IProjectStatusRead]:
    """
    Creates a new project status
    """
    await project_status_checks.project_status_name_is_taken(name=project_status.name)
    new_project_status = await crud.project_status.create(obj_in=project_status)
    return create_response(data=new_project_status)

@router.put("/{id}")
async def update_project_status(
    project_status: IProjectStatusUpdate,
    current_project_status: ProjectStatus = Depends(project_status_deps.get_project_status_by_id_from_path)
) -> IPutResponseBase[IProjectStatusRead]:
    """
    Updates a project status by its id
    """
    if project_status.name:
        await project_status_checks.project_status_name_is_taken(name=project_status.name)
    project_status_updated = await crud.project_status.update(obj_current=current_project_status, obj_new=project_status)
    return create_response(data=project_status_updated)

@router.delete("/{id}")
async def delete_project_status(
        current_project_status: ProjectStatus = Depends(project_status_deps.get_project_status_by_id_from_path)
) -> IDeleteResponseBase[IProjectStatusRead]:
    """
    Deletes a project status by its id
    """
    project_status_deleted = await crud.project_status.remove(id=current_project_status.id)
    return create_response(data=project_status_deleted)