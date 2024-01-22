from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette import status

from app import crud
from app.deps import track_defect_types_deps
from app.models import TrackDefectTypes
from app.schemas.response_schema import (
    ICreateResponseBase,
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPutResponseBase,
    create_response,
)
from app.schemas.track_defect_types import ITrackDefectTypesCreate, ITrackDefectTypesRead
from app.schemas.track_defects import ITrackDefectsRead

router = APIRouter()


@router.get("/list")
async def _get_all_track_defect_types(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[ITrackDefectTypesRead]:
    track_defect_types = await crud.track_defect_types.get_multi_paginated(params=params)
    return create_response(data=track_defect_types)

@router.get("/list/track_defects_by_id/{id}")
async def _get_all_track_defects_by_id(
        id: UUID,
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[ITrackDefectsRead]:
    track_defects = await crud.track_defects.get_by_defect_id_paginated(
        id=id,
        params=params
    )
    return create_response(track_defects)


@router.get("/{track_defect_type_id}")
async def _get_track_defect_type_by_id(
        track_defect_type: TrackDefectTypes = Depends(  # noqa: B008
            track_defect_types_deps.get_track_defect_type_by_id_from_path
        ),
) -> IGetResponseBase[ITrackDefectTypesRead]:
    return create_response(data=track_defect_type)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_track_defect_type(
        new_track_defect_type: ITrackDefectTypesCreate
) -> ICreateResponseBase[ITrackDefectTypesRead]:
    track_defect_type = await crud.track_defect_types.create(obj_in=new_track_defect_type)
    return create_response(track_defect_type)


@router.put("/{track_defect_type_id}")
async def _update_track_defect_type_by_id(
        track_defect_type: ITrackDefectTypesCreate,
        current_track_defect_type: TrackDefectTypes = Depends(  # noqa: B008
            track_defect_types_deps.get_track_defect_type_by_id_from_path
        ),
) -> IPutResponseBase[ITrackDefectTypesRead]:
    updated_track_defect_type = await crud.track_defect_types.update(
        obj_current=current_track_defect_type,
        obj_new=track_defect_type
    )
    return create_response(data=updated_track_defect_type)


@router.delete("/{track_defect_type_id}")
async def _delete_track_defect_type_by_id(
        track_defect_type_id: UUID
) -> IDeleteResponseBase[ITrackDefectTypesRead]:
    track_defect_type = await crud.track_defect_types.remove(id=track_defect_type_id)
    return create_response(data=track_defect_type)
