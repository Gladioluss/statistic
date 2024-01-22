from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params
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

from app.schemas.tower_schema import *

from app.utils.exceptions.common import IdNotFoundException, NameExistException
from app.models.tower import TowerEntity
from app.models.subproject import Subproject
from app.models.status import ObjectStatus
from app.deps import tower_deps, object_status_deps, subproject_deps
from app.utils.checks import tower_checks, object_status_checks, subproject_checks

router = APIRouter()


@router.get("/list")
async def get_towers_list(
        params: Params = Depends()
) -> IGetResponsePaginated[ITowerRead]:
    """
    Gets a paginated list of towers
    """
    towers = await crud.tower.get_multi_paginated(params=params)
    return create_response(data=towers)


@router.get("/list/status")
async def get_towers_list_by_status_id(
        current_object_status: ObjectStatus = Depends(object_status_deps.get_object_status_by_id_from_query),
        params: Params = Depends()
) -> IGetResponsePaginated[ITowerRead]:
    """
    Gets a paginated list of towers by status id
    """
    towers = await crud.tower.get_paginated_list_by_status_id(
        status_id=current_object_status.id,
        params=params
    )
    return create_response(data=towers)


@router.get("/list/object_id")
async def get_towers_list_by_object_id(
        object_id: UUID,
        params: Params = Depends()
) -> IGetResponsePaginated[ITowerRead]:
    """
    Gets a paginated list of towers by object id
    """
    towers = await crud.tower.get_paginated_list_by_object_id(
        object_id=object_id,
        params=params
    )
    return create_response(data=towers)


@router.get("/list/subproject")
async def get_towers_list_by_subproject_id(
        current_subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_query),
        params: Params = Depends()
) -> IGetResponsePaginated[ITowerRead]:
    """
    Gets a paginated list of towers by subproject id
    """
    towers = await crud.tower.get_paginated_list_by_subproject_id(
        subproject_id=current_subproject.id,
        params=params
    )
    return create_response(data=towers)


@router.get("/{id}")
async def read_tower_by_id(
        tower: TowerEntity = Depends(tower_deps.get_tower_by_id_from_path)
) -> IGetResponseBase[ITowerRead]:
    """
    Gets a tower by id
    """
    return create_response(data=tower)


@router.get("/{id}/status")
async def get_tower_with_object_status_by_id(
        tower: TowerEntity = Depends(tower_deps.get_tower_by_id_from_path)
) -> IGetResponseBase[ITowerWithObjectStatusRead]:
    """
    Gets a tower with status by id
    """
    return create_response(data=tower)


@router.get("/{id}/subproject")
async def get_tower_with_subproject_by_id(
        tower: TowerEntity = Depends(tower_deps.get_tower_by_id_from_path)
) -> IGetResponseBase[ITowerWithSubprojectRead]:
    """
    Gets a tower with subproject by id
    """
    return create_response(data=tower)


@router.get("/{id}/full")
async def get_tower_with_subproject_and_status_by_id(
        tower: TowerEntity = Depends(tower_deps.get_tower_by_id_from_path)
) -> IGetResponseBase[ITowerFullInfoRead]:
    """
    Gets a tower with subproject and status by id
    """
    return create_response(data=tower)


@router.post("")
async def create_tower(
        tower: ITowerCreate
) -> IPostResponseBase[ITowerRead]:
    """
    Creates a new tower
    """
    await subproject_checks.subproject_is_exist(id=tower.subproject_id)
    await tower_checks.tower_name_is_taken_in_current_subproject(name=tower.name, subproject_id=tower.subproject_id)
    if tower.status_id:
        await object_status_checks.object_status_is_exist(id=tower.status_id)

    new_tower = await crud.tower.create(obj_in=tower)
    status = await crud.object_status.get(id=new_tower.status_id)

    await rabbit_connection.send_messages(
        headers={
            QueueHeaders.NAME: new_tower.__tablename__,
            QueueHeaders.TYPE: QueueHeaderTypeValues.CREATE,
            QueueHeaders.STATUS: status.name,
        },
        messages=new_tower.to_dict()
    )
    return create_response(data=new_tower)


@router.put("/{id}")
async def update_tower(
    tower: ITowerUpdate,
    current_tower: TowerEntity = Depends(tower_deps.get_tower_by_id_from_path)
) -> IPutResponseBase[ITowerRead]:
    """
    Updates a tower by its id
    """
    if tower.subproject_id:
        await subproject_checks.subproject_is_exist(id=tower.subproject_id)
        if tower.name:
            await tower_checks.tower_name_is_taken_in_current_subproject(name=tower.name,
                                                                         subproject_id=tower.subproject_id)
        if not tower.name:
            await tower_checks.tower_name_is_taken_in_current_subproject(name=current_tower.name,
                                                                         subproject_id=tower.subproject_id)
    if not tower.subproject_id:
        if tower.name:
            await tower_checks.tower_name_is_taken_in_current_subproject(name=tower.name,
                                                                         subproject_id=current_tower.subproject_id)
    if tower.status_id:
        await object_status_checks.object_status_is_exist(id=tower.status_id)

    tower_updated = await crud.tower.update(obj_current=current_tower, obj_new=tower)
    status = await crud.object_status.get(id=tower_updated.status_id)

    await rabbit_connection.send_messages(
        headers={
            QueueHeaders.NAME: tower_updated.__tablename__,
            QueueHeaders.TYPE: QueueHeaderTypeValues.UPDATE,
            QueueHeaders.STATUS: status.name,
        },
        messages=tower_updated.to_dict()
    )
    return create_response(data=tower_updated)


@router.delete("/{id}")
async def delete_tower(
        current_tower: TowerEntity = Depends(tower_deps.get_tower_by_id_from_path)
) -> IDeleteResponseBase[ITowerRead]:
    """
    Deletes a tower by its id
    """
    tower_deleted = await crud.tower.remove(id=current_tower.id)
    return create_response(data=tower_deleted)