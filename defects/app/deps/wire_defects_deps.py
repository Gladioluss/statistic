from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import WireDefects


async def get_wire_defect_by_id_from_path(
    wire_defect_id: Annotated[UUID, Path(description="The UUID id of the WireDefects")]
) -> WireDefects:
    """
    Get a TrackDefects from database by id from the path

    :param wire_defect_id: UUID
    :return: WireDefects
    """

    wire_defect = await crud.wire_defects.get_by_id(id=wire_defect_id)
    if not wire_defect:
        raise IdNotFoundException(WireDefects, incoming_id=wire_defect_id)
    return wire_defect
