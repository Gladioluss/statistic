from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params
from uuid import UUID
from typing import Annotated

from app.deps import object_status_deps
from app.utils.checks import object_status_checks
from app import crud
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    IDeleteResponseBase,
    create_response,
)
from app.schemas.object_status_schema import (
    IObjectStatusRead,
    IObjectStatusUpdate,
    IObjectStatusCreate,
    IObjectStatusWithAllObjectsListRead,
    IObjectStatusWithTowersListRead,
    IObjectStatusWithSpansListRead
)
from app.utils.exceptions.common import IdNotFoundException, NameExistException
from app.models.status import ObjectStatus


router = APIRouter()


@router.get("/list")
async def get_object_statuses(
        params: Params = Depends()
) -> IGetResponsePaginated[IObjectStatusRead]:
    """
    Gets a paginated list of object statuses
    """
    object_statuses = await crud.object_status.get_multi_paginated(params=params)
    return create_response(data=object_statuses)


@router.get("/{id}")
async def read_object_status_by_id(
        object_status: ObjectStatus = Depends(object_status_deps.get_object_status_by_id_from_path)
) -> IGetResponseBase[IObjectStatusRead]:
    """
    Gets an object status by id
    """
    return create_response(data=object_status)


@router.get("/{id}/objects")
async def get_object_status_with_objects_list_by_id(
        object_status: ObjectStatus = Depends(object_status_deps.get_object_status_by_id_from_path)
) -> IGetResponseBase[IObjectStatusWithAllObjectsListRead]:
    """
    Gets object status with all objects list by id
    """
    return create_response(data=object_status)


@router.get("/{id}/towers")
async def get_object_status_with_towers_list_by_id(
        object_status: ObjectStatus = Depends(object_status_deps.get_object_status_by_id_from_path)
) -> IGetResponseBase[IObjectStatusWithTowersListRead]:
    """
    Gets object status with towers list by id
    """
    return create_response(data=object_status)


@router.get("/{id}/spans")
async def get_object_status_with_spans_list_by_id(
        object_status: ObjectStatus = Depends(object_status_deps.get_object_status_by_id_from_path)
) -> IGetResponseBase[IObjectStatusWithSpansListRead]:
    """
    Gets object status with spans list by id
    """
    return create_response(data=object_status)


@router.post("")
async def create_object_status(
        object_status: IObjectStatusCreate
) -> IPostResponseBase[IObjectStatusRead]:
    """
    Creates a new object status
    """
    await object_status_checks.object_status_name_is_taken(name=object_status.name)
    new_object_status = await crud.object_status.create(obj_in=object_status)
    return create_response(data=new_object_status)


@router.put("/{id}")
async def update_object_status(
    object_status: IObjectStatusUpdate,
    current_object_status: ObjectStatus = Depends(object_status_deps.get_object_status_by_id_from_path)
) -> IPutResponseBase[IObjectStatusRead]:
    """
    Updates an object status by its id
    """
    if object_status.name:
        await object_status_checks.object_status_name_is_taken(name=object_status.name)
    object_status_updated = await crud.object_status.update(obj_current=current_object_status, obj_new=object_status)
    return create_response(data=object_status_updated)


@router.delete("/{id}")
async def delete_object_status(
        current_object_status: ObjectStatus = Depends(object_status_deps.get_object_status_by_id_from_path)
) -> IDeleteResponseBase[IObjectStatusRead]:
    """
    Deletes an object status by its id
    """
    object_status_deleted = await crud.object_status.remove(id=current_object_status.id)
    return create_response(data=object_status_deleted)