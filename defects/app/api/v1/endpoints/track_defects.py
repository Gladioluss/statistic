from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette import status

from app import crud
from app.deps import track_defects_deps
from app.models import TrackDefects
from app.schemas.response_schema import (
    ICreateResponseBase,
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPutResponseBase,
    create_response,
)
from app.schemas.track_defects import ITrackDefectsCreate, ITrackDefectsRead

router = APIRouter()


@router.get("/all")
async def _get_all_track_defects(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[ITrackDefectsRead]:
    track_defects = await crud.track_defects.get_multi_paginated(params=params)
    return create_response(data=track_defects)


@router.get("/{track_defect_id}")
async def _get_track_defect_by_id(
        track_defect: TrackDefects = Depends(  # noqa: B008
            track_defects_deps.get_track_defect_by_id_from_path
        ),
) -> IGetResponseBase[ITrackDefectsRead]:
    return create_response(data=track_defect)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_track_defect(
        new_track_defect: ITrackDefectsCreate
) -> ICreateResponseBase[ITrackDefectsRead]:
    track_defect = await crud.track_defects.create(obj_in=new_track_defect)
    return create_response(data=track_defect)


@router.put("/{track_defect_id}")
async def _update_track_defect_by_id(
        track_defect: ITrackDefectsCreate,
        current_track_defect: TrackDefects = Depends(  # noqa: B008
            track_defects_deps.get_track_defect_by_id_from_path
        ),
) -> IPutResponseBase[ITrackDefectsRead]:
    updated_track_defect = await crud.tower_defects.update(
        obj_current=current_track_defect,
        obj_new=track_defect
    )
    return create_response(data=updated_track_defect)


@router.delete("/{track_defect_id}")
async def _delete_track_defect_by_id(
        track_defect_id: UUID
) -> IDeleteResponseBase[ITrackDefectsRead]:
    track_defect = await crud.track_defects.remove(id=track_defect_id)
    return create_response(data=track_defect)
