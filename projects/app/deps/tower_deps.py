from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated

from app import crud
from app.models.tower import TowerEntity
from app.utils.exceptions.common import (
    NameNotFoundException,
    IdNotFoundException,
)


async def get_tower_by_id_from_path(
        id: Annotated[UUID, Path(description="The UUID id of the tower")]
) -> TowerEntity:
    tower = await crud.tower.get(id=id)
    if not tower:
        raise IdNotFoundException(TowerEntity, id=id)
    return tower


async def get_tower_by_id_from_query(
        id: Annotated[UUID, Query(description="The UUID id of the tower")]
) -> TowerEntity:
    tower = await crud.tower.get(id=id)
    if not tower:
        raise IdNotFoundException(TowerEntity, id=id)
    return tower

