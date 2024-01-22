from app import crud
from app.models.work_type import WorkType
from app.utils.exceptions.common import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_work_type_by_id_from_path(
        id: Annotated[UUID, Path(description="The UUID id of the work type")]
) -> WorkType:
    work_type = await crud.work_type.get(id=id)
    if not work_type:
        raise IdNotFoundException(WorkType, id=id)
    return work_type


async def get_work_type_by_id_from_query(
        id: Annotated[UUID, Query(description="The UUID id of the work type")]
) -> WorkType:
    work_type = await crud.work_type.get(id=id)
    if not work_type:
        raise IdNotFoundException(WorkType, id=id)
    return work_type