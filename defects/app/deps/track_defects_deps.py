from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import TrackDefects


async def get_track_defect_by_id_from_path(
    track_defect_id: Annotated[UUID, Path(description="The UUID id of the TrackDefects")]
) -> TrackDefects:
    """
    Get a TrackDefects from database by id from the path

    :param track_defect_id: UUID
    :return: TrackDefects
    """

    track_defect = await crud.track_defects.get_by_id(id=track_defect_id)
    if not track_defect:
        raise IdNotFoundException(TrackDefects, incoming_id=track_defect_id)
    return track_defect
