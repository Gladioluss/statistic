from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette import status

from app import crud
from app.deps import wire_defect_types_deps
from app.models import WireDefectTypes
from app.schemas.response_schema import (
    ICreateResponseBase,
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPutResponseBase,
    create_response,
)
from app.schemas.track_defect_types import ITrackDefectTypesRead
from app.schemas.wire_defect_types import IWireDefectTypesCreate, IWireDefectTypesRead
from app.schemas.wire_defects import IWireDefectsRead
from app.schemas.wire_defects_history import IWireDefectsHistoryRead

router = APIRouter()


@router.get("/list")
async def _get_all_wire_defect_type(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IWireDefectTypesRead]:
    wire_defect_types = await crud.wire_defect_types.get_multi_paginated(params=params)
    return create_response(data=wire_defect_types)


@router.get("/list/wire_defects_by_id/{id}")
async def _get_all_wire_defects_by_id(
        id: UUID,
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IWireDefectsRead]:
    wire_defects = await crud.wire_defects.get_by_defect_id_paginated(
        id=id,
        params=params
    )
    return create_response(data=wire_defects)


@router.get("/list/wire_defects_history_by_id/{id}")
async def _get_all_wire_defects_by_id(
        id: UUID,
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IWireDefectsHistoryRead]:
    wire_defects_history = await crud.tower_defects_history.get_by_defect_id_paginated(
        id=id,
        params=params
    )
    return create_response(wire_defects_history)


@router.get("/{wire_defect_type_id}")
async def _get_wire_defect_type_by_id(
        wire_defect_type: WireDefectTypes = Depends(  # noqa: B008
            wire_defect_types_deps.get_wire_defect_type_by_id_from_path
        ),
) -> IGetResponseBase[IWireDefectTypesRead]:
    return create_response(data=wire_defect_type)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_wire_defect_type(
        new_wire_defect_type: IWireDefectTypesCreate
) -> ICreateResponseBase[IWireDefectTypesRead]:
    wire_defect_type = await crud.wire_defect_types.create(obj_in=new_wire_defect_type)
    return create_response(wire_defect_type)


@router.put("/{wire_defect_type_id}")
async def _update_wire_defect_type_by_id(
        wire_defect_type: IWireDefectTypesCreate,
        current_wire_defect_type: WireDefectTypes = Depends(  # noqa: B008
            wire_defect_types_deps.get_wire_defect_type_by_id_from_path
        ),
) -> IPutResponseBase[IWireDefectTypesRead]:
    updated_wire_defect_type = await crud.wire_defect_types.update(
        obj_current=current_wire_defect_type,
        obj_new=wire_defect_type
    )
    return create_response(data=updated_wire_defect_type)


@router.delete("/{wire_defect_type_id}")
async def _delete_wire_defect_type_by_id(
        wire_defect_type_id: UUID
) -> IDeleteResponseBase[ITrackDefectTypesRead]:
    wire_defect_type = await crud.wire_defect_types.remove(id=wire_defect_type_id)
    return create_response(data=wire_defect_type)
