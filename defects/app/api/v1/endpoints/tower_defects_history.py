from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params

from app import crud
from app.deps import tower_defects_history_deps
from app.models import TowerDefectsHistory
from app.schemas.response_schema import IDeleteResponseBase, IGetResponseBase, IGetResponsePaginated, create_response
from app.schemas.tower_defects_history import ITowerDefectsHistoryRead

router = APIRouter()


@router.get("/list")
async def _get_all_tower_defects_history(
        params: Params = Depends() # noqa: B008
) -> IGetResponsePaginated[ITowerDefectsHistoryRead]:
    tower_defects_history = await crud.tower_defects_history.get_multi_paginated(params=params)
    return create_response(data=tower_defects_history)


@router.get("/{tower_defects_history_id}")
async def _get_tower_defects_history_by_id(
        tower_defects_history: TowerDefectsHistory = Depends(  # noqa: B008
            tower_defects_history_deps.get_tower_defects_history_by_id_from_path
        ),
) -> IGetResponseBase[ITowerDefectsHistoryRead]:
    return create_response(data=tower_defects_history)


@router.delete("/{tower_defects_history_id}")
async def _delete_tower_defects_history_by_id(
        tower_defects_history_id: UUID
) -> IDeleteResponseBase[ITowerDefectsHistoryRead]:
    tower_defects_history = await crud.tower_defects_history.remove(id=tower_defects_history_id)
    return create_response(data=tower_defects_history)
