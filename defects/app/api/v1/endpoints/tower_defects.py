from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette import status

from app import crud
from app.core.rabbit.queue_message_settings import QueueHeaders, QueueHeaderTypeValues
from app.core.rabbit.rabbit_connection import rabbit_connection
from app.deps import tower_defects_deps
from app.models import TowerDefects
from app.schemas.response_schema import (
    ICreateResponseBase,
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPutResponseBase,
    create_response,
)
from app.schemas.tower_defects import ITowerDefectsCreate, ITowerDefectsRead

router = APIRouter()


@router.get("/list")
async def _get_all_tower_defects(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[ITowerDefectsRead]:
    tower_defects = await crud.tower_defects.get_multi_paginated(params=params)
    return create_response(data=tower_defects)


@router.get("/{tower_defect_id}")
async def _get_tower_defect_by_id(
        tower_defect: TowerDefects = Depends(  # noqa: B008
            tower_defects_deps.get_tower_defect_by_id_from_path
        ),
) -> IGetResponseBase[ITowerDefectsRead]:
    return create_response(data=tower_defect)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_tower_defect(
        new_tower_defect: ITowerDefectsCreate
) -> ICreateResponseBase[ITowerDefectsRead]:
    tower_defect = await crud.tower_defects.create(obj_in=new_tower_defect)
    await rabbit_connection.send_messages(
        headers={
            QueueHeaders.NAME: tower_defect.__tablename__,
            QueueHeaders.TYPE: QueueHeaderTypeValues.CREATE
        },
        messages=tower_defect.to_dict()
    )
    return create_response(data=tower_defect)


@router.put("/{tower_defect_id}")
async def _update_tower_defect_by_id(
        tower_defect: ITowerDefectsCreate,
        current_tower_defect: TowerDefects = Depends(  # noqa: B008
            tower_defects_deps.get_tower_defect_by_id_from_path
        ),
) -> IPutResponseBase[ITowerDefectsRead]:
    updated_tower_defect = await crud.tower_defects.update(
        obj_current=current_tower_defect,
        obj_new=tower_defect
    )
    return create_response(data=updated_tower_defect)


@router.delete("/{tower_defect_id}")
async def _delete_tower_defect_by_id(
        tower_defect_id: UUID
) -> IDeleteResponseBase[ITowerDefectsRead]:
    tower_defect = await crud.tower_defects.remove(id=tower_defect_id)
    await crud.tower_defects_history.create_from_tower_defects_obj(obj_in=tower_defect)
    return create_response(data=tower_defect)
