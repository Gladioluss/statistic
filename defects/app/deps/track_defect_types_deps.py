from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import TrackDefectTypes


async def get_track_defect_type_by_id_from_path(
    track_defect_type_id: Annotated[UUID, Path(description="The UUID id of the TrackDefectTypes")]
) -> TrackDefectTypes:
    """
    Get a TrackDefectTypes from database by id from the path

    :param track_defect_type_id: UUID
    :return: TrackDefectTypes
    """

    track_defect_type = await crud.track_defect_types.get_by_id(id=track_defect_type_id)
    if not track_defect_type:
        raise IdNotFoundException(TrackDefectTypes, incoming_id=track_defect_type_id)
    return track_defect_type
