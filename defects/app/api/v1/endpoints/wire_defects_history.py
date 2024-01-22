from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params

from app import crud
from app.deps import wire_defects_history_deps
from app.models import WireDefectsHistory
from app.schemas.response_schema import IDeleteResponseBase, IGetResponseBase, IGetResponsePaginated, create_response
from app.schemas.wire_defects_history import IWireDefectsHistoryRead

router = APIRouter()


@router.get("/list")
async def _get_all_wire_defects_history(
        params: Params = Depends() # noqa: B008
) -> IGetResponsePaginated[IWireDefectsHistoryRead]:
    wire_defects_history = await crud.wire_defects_history.get_multi_paginated(params=params)
    return create_response(data=wire_defects_history)


@router.get("/{wire_defects_history_id}")
async def _get_wire_defects_history_by_id(
        wire_defects_history: WireDefectsHistory = Depends(  # noqa: B008
            wire_defects_history_deps.get_wire_defects_history_by_id_from_path
        ),
) -> IGetResponseBase[IWireDefectsHistoryRead]:
    return create_response(data=wire_defects_history)


@router.delete("/{wire_defects_history_id}")
async def _delete_wire_defects_history_by_id(
        wire_defects_history_id: UUID
) -> IDeleteResponseBase[IWireDefectsHistoryRead]:
    wire_defects_history = await crud.wire_defects_history.remove(id=wire_defects_history_id)
    return create_response(data=wire_defects_history)
