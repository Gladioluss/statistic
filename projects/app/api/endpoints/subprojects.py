from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params
from uuid import UUID
from typing import Annotated

from app import crud
from app.core.rabbit.queue_message_settings import QueueHeaders, QueueHeaderTypeValues
from app.core.rabbit.rabbit_connection import rabbit_connection
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
    IDeleteResponseBase
)

from app.schemas.subproject_schema import (
    ISubprojectCreate,
    ISubprojectRead,
    ISubprojectUpdate,
    ISubprojectWithProjectRead,
    ISubprojectFullInfoRead,
    ISubprojectWithStatusRead,
    ISubprojectWithWorkTypeRead
)
from app.utils.exceptions.common import IdNotFoundException, NameExistException
from app.models.subproject import Subproject
from app.models.status import ProjectStatus
from app.models.project import Project
from app.models.work_type import WorkType
from app.deps import subproject_deps, project_status_deps, work_type_deps, project_deps
from app.utils.checks import subproject_checks, project_status_checks, work_type_checks, project_checks

router = APIRouter()


@router.get("/list")
async def get_subprojects(
        params: Params = Depends()
) -> IGetResponsePaginated[ISubprojectRead]:
    """
    Gets a paginated list of subprojects
    """
    subprojects = await crud.subproject.get_multi_paginated(params=params)
    return create_response(data=subprojects)


@router.get("/list/projects_status")
async def get_subprojects_list_by_project_status_id(
        current_project_status: ProjectStatus = Depends(project_status_deps.get_project_status_by_id_from_query),
        params: Params = Depends()
) -> IGetResponsePaginated[ISubprojectRead]:
    """
    Gets a paginated list of subprojects by status id
    """
    subprojects = await crud.subproject.get_paginated_list_by_status_id(
        status_id=current_project_status.id,
        params=params
    )
    return create_response(data=subprojects)


@router.get("/list/work_type")
async def get_subprojects_list_by_work_type_id(
        current_work_type: WorkType = Depends(work_type_deps.get_work_type_by_id_from_query),
        params: Params = Depends()
) -> IGetResponsePaginated[ISubprojectRead]:
    """
    Gets a paginated list of subprojects by work type id
    """
    subprojects = await crud.subproject.get_paginated_list_by_work_type_id(
        work_type_id=current_work_type.id,
        params=params
    )
    return create_response(data=subprojects)


@router.get("/list/project")
async def get_subprojects_list_by_project_id(
        current_project: Project = Depends(project_deps.get_project_by_id_from_query),
        params: Params = Depends()
) -> IGetResponsePaginated[ISubprojectRead]:
    """
    Gets a paginated list of subprojects by project id
    """
    subprojects = await crud.subproject.get_paginated_list_by_project_id(
        project_id=current_project.id,
        params=params
    )
    return create_response(data=subprojects)


@router.get("/{id}")
async def read_subproject_by_id(
        subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_path)
) -> IGetResponseBase[ISubprojectRead]:
    """
    Gets a subproject by id
    """
    return create_response(data=subproject)


@router.get("/{id}/status")
async def get_subproject_with_status_by_id(
        subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_path)
) -> IGetResponseBase[ISubprojectWithStatusRead]:
    """
    Gets a subproject with status by id
    """
    return create_response(data=subproject)


@router.get("/{id}/project")
async def get_subproject_with_project_by_id(
        subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_path)
) -> IGetResponseBase[ISubprojectWithProjectRead]:
    """
    Gets a subproject with project by id
    """
    return create_response(data=subproject)


@router.get("/{id}/work_type")
async def get_subproject_with_work_type_by_id(
        subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_path)
) -> IGetResponseBase[ISubprojectWithWorkTypeRead]:
    """
    Gets a subproject with work type by id
    """
    return create_response(data=subproject)


@router.get("/{id}/full")
async def get_subproject_with_full_info_by_id(
        subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_path)
) -> IGetResponseBase[ISubprojectFullInfoRead]:
    """
    Gets a subproject with work type by id
    """
    return create_response(data=subproject)


@router.post("")
async def create_subproject(
        subproject: ISubprojectCreate
) -> IPostResponseBase[ISubprojectRead]:
# ):
    """
    Creates a new subproject
    """
    await project_checks.project_is_exist(id=subproject.project_id)
    await subproject_checks.subproject_name_is_taken_in_current_project(
        name=subproject.name,
        project_id=subproject.project_id
    )

    if subproject.work_type_id:
        await work_type_checks.work_type_is_exist(id=subproject.work_type_id)
    if subproject.status_id:
        await project_status_checks.project_status_is_exist(id=subproject.status_id)

    new_subproject = await crud.subproject.create(obj_in=subproject)
    await rabbit_connection.send_messages(
        headers={
            QueueHeaders.NAME: new_subproject.__tablename__,
            QueueHeaders.TYPE: QueueHeaderTypeValues.CREATE
            },
        messages=new_subproject.to_dict()
    )
    # return new_subproject
    return create_response(data=new_subproject)


@router.put("/{id}")
async def update_subproject(
    subproject: ISubprojectUpdate,
    current_subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_path)
) -> IPutResponseBase[ISubprojectRead]:
    """
    Updates a subproject by its id
    """
    if subproject.project_id:
        await project_checks.project_is_exist(id=subproject.project_id)
        if subproject.name:
            await subproject_checks.subproject_name_is_taken_in_current_project(
                name=subproject.name,
                project_id=subproject.project_id
            )
        if not subproject.name:
            await subproject_checks.subproject_name_is_taken_in_current_project(
                name=current_subproject.name,
                project_id=subproject.project_id
            )

    if not subproject.project_id:
        if subproject.name:
            await subproject_checks.subproject_name_is_taken_in_current_project(
                name=subproject.name,
                project_id=current_subproject.project_id
            )

    if subproject.work_type_id:
        await work_type_checks.work_type_is_exist(id=subproject.work_type_id)
    if subproject.status_id:
        await project_status_checks.project_status_is_exist(id=subproject.status_id)

    subproject_updated = await crud.subproject.update(obj_current=current_subproject, obj_new=subproject)
    await rabbit_connection.send_messages(
        headers={
            QueueHeaders.NAME: subproject_updated.__tablename__,
            QueueHeaders.TYPE: QueueHeaderTypeValues.UPDATE
        },
        messages=subproject_updated.to_dict()
    )
    return create_response(data=subproject_updated)


@router.delete("/{id}")
async def delete_subproject(
        current_subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_path)
) -> IDeleteResponseBase[ISubprojectRead]:
    """
    Deletes a subproject by its id
    """
    subproject_deleted = await crud.subproject.remove(id=current_subproject.id)
    return create_response(data=subproject_deleted)