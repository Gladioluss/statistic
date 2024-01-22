from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import TowerDefectsHistory


async def get_tower_defects_history_by_id_from_path(
    tower_defects_history_id: Annotated[UUID, Path(description="The UUID id of the StringDefectsHistory")]
) -> TowerDefectsHistory:
    """
    Get a StringDefectsHistory from database by id from the path

    :param tower_defects_history_id: UUID
    :return: StringDefectsHistory
    """

    tower_defects_history= await crud.tower_defects_history.get_by_id(id=tower_defects_history_id)
    if not tower_defects_history:
        raise IdNotFoundException(TowerDefectsHistory, incoming_id=tower_defects_history_id)
    return tower_defects_history
