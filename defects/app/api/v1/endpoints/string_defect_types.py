from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette import status

from app import crud
from app.deps import string_defect_types_deps
from app.models import StringDefectTypes
from app.schemas.response_schema import (
    ICreateResponseBase,
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPutResponseBase,
    create_response,
)
from app.schemas.string_defect_types import IStringDefectTypesCreate, IStringDefectTypesRead
from app.schemas.string_defects import IStringDefectsRead
from app.schemas.string_defects_history import IStringDefectsHistoryRead

router = APIRouter()


@router.get("/list")
async def _get_all_string_defect_types(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IStringDefectTypesRead]:
    string_defect_types = await crud.string_defect_types.get_multi_paginated(params=params)
    return create_response(data=string_defect_types)


@router.get("/list/string_defects_by_id/{id}")
async def _get_all_string_defects_by_id(
        id: UUID,
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IStringDefectsRead]:
    string_defects = await crud.string_defects.get_by_defect_id_paginated(
        id=id,
        params=params
    )
    return create_response(data=string_defects)


@router.get("/list/string_defects_history_by_id/{id}")
async def _get_all_string_defects_by_id(
        id: UUID,
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IStringDefectsHistoryRead]:
    string_defects_history = await crud.string_defects_history.get_by_defect_id_paginated(
        id=id,
        params=params
    )
    return create_response(data=string_defects_history)


@router.get("/{string_defect_type_id}")
async def _get_string_defect_type_by_id(
        string_defect_type: StringDefectTypes = Depends(  # noqa: B008
            string_defect_types_deps.get_string_defect_type_by_id_from_path
        ),
) -> IGetResponseBase[IStringDefectTypesRead]:
    return create_response(data=string_defect_type)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_string_defect_type(
        new_string_defect_type: IStringDefectTypesCreate
) -> ICreateResponseBase[IStringDefectTypesRead]:
    string_defect_type = await crud.string_defect_types.create(obj_in=new_string_defect_type)
    return create_response(data=string_defect_type)


@router.put("/{string_defect_type_id}")
async def _update_string_defect_type_by_id(
        string_defect_type: IStringDefectTypesCreate,
        current_string_defect_type: StringDefectTypes = Depends(  # noqa: B008
            string_defect_types_deps.get_string_defect_type_by_id_from_path
        ),
) -> IPutResponseBase[IStringDefectTypesRead]:
    updated_string_defect_type = await crud.string_defect_types.update(
        obj_current=current_string_defect_type,
        obj_new=string_defect_type
    )
    return create_response(data=updated_string_defect_type)


@router.delete("/{string_defect_type_id}")
async def _delete_string_defect_type_by_id(
        string_defect_type_id: UUID
) -> IDeleteResponseBase[IStringDefectTypesRead]:
    string_defect_type = await crud.string_defect_types.remove(id=string_defect_type_id)
    return create_response(data=string_defect_type)
