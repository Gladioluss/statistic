from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette import status

from app import crud
from app.deps import wire_defects_deps
from app.models import WireDefects
from app.schemas.response_schema import (
    ICreateResponseBase,
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPutResponseBase,
    create_response,
)
from app.schemas.wire_defects import IWireDefectsCreate, IWireDefectsRead

router = APIRouter()


@router.get("/list")
async def _get_all_wire_defects(
        params: Params = Depends() # noqa: B008
) -> IGetResponsePaginated[IWireDefectsRead]:
    wire_defects = await crud.wire_defects.get_multi_paginated(params=params)
    return create_response(wire_defects)


@router.get("/{wire_defect_id}")
async def _get_wire_defect_by_id(
        wire_defect: WireDefects = Depends(  # noqa: B008
            wire_defects_deps.get_wire_defect_by_id_from_path
        ),
) -> IGetResponseBase[IWireDefectsRead]:
    return create_response(data=wire_defect)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_wire_defect(
        new_wire_defect: IWireDefectsCreate
) -> ICreateResponseBase[IWireDefectsRead]:
    wire_defect = await crud.wire_defects.create(obj_in=new_wire_defect)
    return create_response(wire_defect)


@router.put("/{wire_defect_id}")
async def _update_wire_defect_by_id(
        wire_defect: IWireDefectsCreate,
        current_wire_defect: WireDefects = Depends(  # noqa: B008
            wire_defects_deps.get_wire_defect_by_id_from_path
        ),
) -> IPutResponseBase[IWireDefectsRead]:
    updated_wire_defect = await crud.wire_defects.update(
        obj_current=current_wire_defect,
        obj_new=wire_defect
    )
    return create_response(data=updated_wire_defect)


@router.delete("/{wire_defect_id}")
async def _delete_wire_defect_by_id(
        wire_defect_id: UUID
) -> IDeleteResponseBase[IWireDefectsRead]:
    wire_defect = await crud.wire_defects.remove(id=wire_defect_id)
    await crud.wire_defects_history.create_from_wire_defects_obj(obj_in=wire_defect)
    return create_response(data=wire_defect)
