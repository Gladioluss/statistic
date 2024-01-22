from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette import status

from app import crud
from app.deps import tower_defect_types_deps
from app.models import TowerDefectTypes
from app.schemas.response_schema import (
    ICreateResponseBase,
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPutResponseBase,
    create_response,
)
from app.schemas.tower_defect_types import ITowerDefectTypesCreate, ITowerDefectTypesRead
from app.schemas.tower_defects import ITowerDefectsRead
from app.schemas.tower_defects_history import ITowerDefectsHistoryRead

router = APIRouter()


@router.get("/list")
async def _get_all_tower_defect_types(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[ITowerDefectTypesRead]:
    tower_defect_types = await crud.tower_defect_types.get_multi_paginated(params=params)
    return create_response(tower_defect_types)


@router.get("/list/tower_defects_by_id/{id}")
async def _get_all_tower_defects_by_id(
        id: UUID,
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[ITowerDefectsRead]:
    tower_defects = await crud.tower_defects.get_by_defect_id_paginated(
        id=id,
        params=params
    )
    return create_response(tower_defects)


@router.get("/list/tower_defects_history_by_id/{id}")
async def _get_all_tower_defects_by_id(
        id: UUID,
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[ITowerDefectsHistoryRead]:
    tower_defects_history = await crud.tower_defects_history.get_by_defect_id_paginated(
        id=id,
        params=params
    )
    return create_response(data=tower_defects_history)


@router.get("/{tower_defect_type_id}")
async def _get_tower_defect_type_by_id(
        tower_defect_type: TowerDefectTypes = Depends(  # noqa: B008
            tower_defect_types_deps.get_tower_defect_type_by_id_from_path
        ),
) -> IGetResponseBase[ITowerDefectTypesRead]:
    return create_response(data=tower_defect_type)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_tower_defect_type(
        new_tower_defect_type: ITowerDefectTypesCreate
) -> ICreateResponseBase[ITowerDefectTypesRead]:
    string_defect_type = await crud.tower_defect_types.create(obj_in=new_tower_defect_type)
    return create_response(string_defect_type)


@router.put("/{tower_defect_type_id}")
async def _update_tower_defect_type_by_id(
        tower_defect_type: ITowerDefectTypesCreate,
        current_tower_defect_type: TowerDefectTypes = Depends(  # noqa: B008
            tower_defect_types_deps.get_tower_defect_type_by_id_from_path
        ),
) -> IPutResponseBase[ITowerDefectTypesRead]:
    updated_tower_defect_type = await crud.tower_defect_types.update(
        obj_current=current_tower_defect_type,
        obj_new=tower_defect_type
    )
    return create_response(data=updated_tower_defect_type)


@router.delete("/{tower_defect_type_id}")
async def _delete_tower_defect_type_by_id(
        tower_defect_type_id: UUID
) -> IDeleteResponseBase[ITowerDefectTypesRead]:
    tower_defect_type = await crud.tower_defect_types.remove(id=tower_defect_type_id)
    return create_response(data=tower_defect_type)
