from app import crud
from app.models.status import ObjectStatus
from app.utils.exceptions.common import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_object_status_by_name_from_path(
        name: Annotated[str, Path(description="String compare with name")]
) -> ObjectStatus:
    object_status = await crud.object_status.get_by_name(name=name)
    if not object_status:
        raise NameNotFoundException(ObjectStatus, name=name)
    return object_status


async def get_object_status_by_id_from_path(
        id: Annotated[UUID, Path(description="The UUID id of the object status")]
) -> ObjectStatus:
    object_status = await crud.object_status.get(id=id)
    if not object_status:
        raise IdNotFoundException(ObjectStatus, id=id)
    return object_status


async def get_object_status_by_id_from_query(
        id: Annotated[UUID, Query(description="The UUID id of the object status")]
) -> ObjectStatus:
    object_status = await crud.object_status.get(id=id)
    if not object_status:
        raise IdNotFoundException(ObjectStatus, id=id)
    return object_status