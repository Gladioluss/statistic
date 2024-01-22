from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params
from uuid import UUID
from typing import Annotated

from app import crud
from app.deps import work_type_deps
from app.utils.checks import work_type_checks
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
    IDeleteResponseBase
)
from app.schemas.work_type_schema import (
    IWorkTypeRead,
    IWorkTypeWithSubprojectsRead,
    IWorkTypeCreate, 
    IWorkTypeUpdate
)
from app.models.work_type import WorkType
from app.utils.exceptions.common import IdNotFoundException, NameExistException

router = APIRouter()


@router.get("")
async def get_work_types(
        params: Params = Depends()
) -> IGetResponsePaginated[IWorkTypeRead]:
    """
    Gets a paginated list of work types
    """
    work_types = await crud.work_type.get_multi_paginated(params=params)
    return create_response(data=work_types)


@router.get("/{id}")
async def read_work_type_by_id(
        work_type: WorkType = Depends(work_type_deps.get_work_type_by_id_from_path)
) -> IGetResponseBase[IWorkTypeRead]:
    """
    Gets a work type by id
    """
    return create_response(data=work_type)


@router.get("/{id}/subprojects")
async def get_work_type_with_subprojects_list_by_id(
        work_type: WorkType = Depends(work_type_deps.get_work_type_by_id_from_path)
) -> IGetResponseBase[IWorkTypeWithSubprojectsRead]:
    """
    Gets a work type with list of subprojects by id
    """
    return create_response(data=work_type)


@router.post("")
async def create_work_type(
        work_type: IWorkTypeCreate
) -> IPostResponseBase[IWorkTypeRead]:
    """
    Creates a new work type
    """
    await work_type_checks.work_type_name_is_taken(name=work_type.name)
    new_work_type = await crud.work_type.create(obj_in=work_type)
    return create_response(data=new_work_type)


@router.put("/{id}")
async def update_work_type(
    work_type: IWorkTypeUpdate,
    current_work_type: WorkType = Depends(work_type_deps.get_work_type_by_id_from_path)
) -> IPutResponseBase[IWorkTypeRead]:
    """
    Updates a work type by its id
    """
    if work_type.name:
        await work_type_checks.work_type_name_is_taken(name=work_type.name)

    work_type_updated = await crud.work_type.update(obj_current=current_work_type, obj_new=work_type)
    return create_response(data=work_type_updated)


@router.delete("/{id}")
async def delete_work_type(
        current_work_type: WorkType = Depends(work_type_deps.get_work_type_by_id_from_path)
) -> IDeleteResponseBase[IWorkTypeRead]:
    """
    Deletes a work type by its id
    """
    work_type_deleted = await crud.work_type.remove(id=current_work_type.id)
    return create_response(data=work_type_deleted)