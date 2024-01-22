from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import WireDefectTypes


async def get_wire_defect_type_by_id_from_path(
    wire_defect_type_id: Annotated[UUID, Path(description="The UUID id of the WireDefectTypes")]
) -> WireDefectTypes:
    """
    Get a TrackDefectTypes from database by id from the path

    :param wire_defect_type_id: UUID
    :return: WireDefectTypes
    """

    wire_defect_type = await crud.wire_defect_types.get_by_id(id=wire_defect_type_id)
    if not wire_defect_type:
        raise IdNotFoundException(WireDefectTypes, incoming_id=wire_defect_type_id)
    return wire_defect_type
