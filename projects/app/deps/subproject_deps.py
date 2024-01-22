from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated

from app import crud
from app.models.subproject import Subproject
from app.utils.exceptions.common import (
    NameNotFoundException,
    IdNotFoundException,
)

async def get_subproject_by_name_from_path(
        name: Annotated[
            str, Path(description="String compare with name")
        ]
) -> Subproject:
    subproject = await crud.subproject.get_by_name(name=name)
    if not subproject:
        raise NameNotFoundException(Subproject, name=name)
    return subproject

async def get_subproject_by_id_from_path(
        id: Annotated[UUID, Path(description="The UUID id of the subproject")]
) -> Subproject:
    subproject = await crud.subproject.get(id=id)
    if not subproject:
        raise IdNotFoundException(Subproject, id=id)
    return subproject


async def get_subproject_by_id_from_query(
        id: Annotated[UUID, Query(description="The UUID id of the subproject")]
) -> Subproject:
    subproject = await crud.subproject.get(id=id)
    if not subproject:
        raise IdNotFoundException(Subproject, id=id)
    return subproject