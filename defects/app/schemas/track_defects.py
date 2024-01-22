from uuid import UUID

from app.models.track_defects import TrackDefectsBase
from app.utils.partial import optional


class ITrackDefectsCreate(TrackDefectsBase):
    pass


class ITrackDefectsRead(TrackDefectsBase):
    id: UUID


@optional
class ITrackDefectsUpdate(TrackDefectsBase):
    pass
