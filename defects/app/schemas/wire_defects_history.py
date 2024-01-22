from uuid import UUID

from app.models.wire_defects_history import WireDefectsHistoryBase
from app.utils.partial import optional


class IWireDefectsHistoryCreate(WireDefectsHistoryBase):
    pass


class IWireDefectsHistoryRead(WireDefectsHistoryBase):
    id: UUID


@optional
class IWireDefectsHistoryUpdate(WireDefectsHistoryBase):
    pass
