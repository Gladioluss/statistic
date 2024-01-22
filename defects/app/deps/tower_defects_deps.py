from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import TowerDefects


async def get_tower_defect_by_id_from_path(
    tower_defect_id: Annotated[UUID, Path(description="The UUID id of the TowerDefects")]
) -> TowerDefects:
    """
    Get a TowerDefects from database by id from the path

    :param tower_defect_id: UUID
    :return: StringDefects
    """

    tower_defect = await crud.string_defects.get_by_id(id=tower_defect_id)
    if not tower_defect:
        raise IdNotFoundException(TowerDefects, incoming_id=tower_defect_id)
    return tower_defect
