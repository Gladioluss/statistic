from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params

from app import crud
from app.deps import string_defects_history_deps
from app.models import StringDefectsHistory
from app.schemas.response_schema import IDeleteResponseBase, IGetResponseBase, IGetResponsePaginated, create_response
from app.schemas.string_defects_history import IStringDefectsHistoryRead

router = APIRouter()


@router.get("/list")
async def _get_all_string_defects_history(
        params: Params = Depends() # noqa: B008
) -> IGetResponsePaginated[IStringDefectsHistoryRead]:
    string_defects_history = await crud.string_defects_history.get_multi_paginated(params=params)
    return create_response(data=string_defects_history)


@router.get("/{string_defects_history_id}")
async def _get_string_defects_history_by_id(
        string_defects_history: StringDefectsHistory = Depends(  # noqa: B008
            string_defects_history_deps.get_string_defects_history_by_id_from_path
        ),
) -> IGetResponseBase[IStringDefectsHistoryRead]:
    return create_response(data=string_defects_history)


@router.delete("/{string_defects_history_id}")
async def _delete_string_defects_history_by_id(
        string_defects_history_id: UUID
) -> IDeleteResponseBase[IStringDefectsHistoryRead]:
    string_defects_history = await crud.string_defects_history.remove(id=string_defects_history_id)
    return create_response(data=string_defects_history)
