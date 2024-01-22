from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import WireDefectsHistory


async def get_wire_defects_history_by_id_from_path(
    wire_defects_history_id: Annotated[UUID, Path(description="The UUID id of the WireDefectsHistory")]
) -> WireDefectsHistory:
    """
    Get a WireDefectsHistory from database by id from the path

    :param wire_defects_history_id: UUID
    :return: WireDefectsHistory
    """

    wire_defects_history= await crud.wire_defects_history.get_by_id(id=wire_defects_history_id)
    if not wire_defects_history:
        raise IdNotFoundException(WireDefectsHistory, incoming_id=wire_defects_history_id)
    return wire_defects_history
