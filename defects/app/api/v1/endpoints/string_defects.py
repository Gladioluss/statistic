from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette import status

from app import crud
from app.deps import string_defects_deps
from app.models import StringDefects
from app.schemas.response_schema import (
    ICreateResponseBase,
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPutResponseBase,
    create_response,
)
from app.schemas.string_defects import IStringDefectsCreate, IStringDefectsRead

router = APIRouter()


@router.get("/list")
async def _get_all_string_defects(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IStringDefectsRead]:
    string_defects = await crud.string_defects.get_multi_paginated(params=params)
    return create_response(data=string_defects)


@router.get("/{string_defect_id}")
async def _get_string_defects_by_id(
        string_defect: StringDefects = Depends(  # noqa: B008
            string_defects_deps.get_string_defect_by_id_from_path
        ),
) -> IGetResponseBase[IStringDefectsRead]:
    return create_response(data=string_defect)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_string_defects(
        new_string_defect: IStringDefectsCreate
) -> ICreateResponseBase[IStringDefectsRead]:
    string_defect = await crud.string_defects.create(obj_in=new_string_defect)
    return create_response(data=string_defect)


@router.put("/{string_defect_id}")
async def _update_string_defects_by_id(
        string_defect: IStringDefectsCreate,
        current_string_defect: StringDefects = Depends(  # noqa: B008
            string_defects_deps.get_string_defect_by_id_from_path
        ),
) -> IPutResponseBase[IStringDefectsRead]:
    updated_string_defect = await crud.string_defects.update(
        obj_current=current_string_defect,
        obj_new=string_defect
    )
    return create_response(data=updated_string_defect)


@router.delete("/{string_defect_id}")
async def _delete_string_defects_by_id(
        string_defect_id: UUID
) -> IDeleteResponseBase[IStringDefectsRead]:
    string_defect = await crud.string_defects.remove(id=string_defect_id)
    await crud.string_defects_history.create_from_string_defects_obj(obj_in=string_defect)
    return create_response(data=string_defect)
