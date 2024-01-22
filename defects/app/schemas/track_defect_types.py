from uuid import UUID

from app.models.track_defect_types import TrackDefectTypesBase
from app.utils.partial import optional


class ITrackDefectTypesCreate(TrackDefectTypesBase):
    pass


class ITrackDefectTypesRead(TrackDefectTypesBase):
    id: UUID


@optional
class ITrackDefectTypesUpdate(TrackDefectTypesBase):
    pass
