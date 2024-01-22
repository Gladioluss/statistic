from uuid import UUID

from app.models.wire_defects import WireDefectsBase
from app.utils.partial import optional


class IWireDefectsCreate(WireDefectsBase):
    pass


class IWireDefectsRead(WireDefectsBase):
    id: UUID


@optional
class IWireDefectsUpdate(WireDefectsBase):
    pass
