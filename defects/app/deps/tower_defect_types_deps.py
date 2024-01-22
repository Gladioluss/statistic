from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import TowerDefectTypes


async def get_tower_defect_type_by_id_from_path(
    tower_defect_type_id: Annotated[UUID, Path(description="The UUID id of the TowerDefectTypes")]
) -> TowerDefectTypes:
    """
    Get a TowerDefectTypes from database by id from the path

    :param tower_defect_type_id: UUID
    :return: TowerDefectTypes
    """

    tower_defect_type = await crud.tower_defect_types.get_by_id(id=tower_defect_type_id)
    if not tower_defect_type:
        raise IdNotFoundException(TowerDefectTypes, incoming_id=tower_defect_type_id)
    return tower_defect_type
