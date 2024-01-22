from uuid import UUID

from app.models.wire_defect_types import WireDefectTypesBase
from app.utils.partial import optional


class IWireDefectTypesCreate(WireDefectTypesBase):
    pass


class IWireDefectTypesRead(WireDefectTypesBase):
    id: UUID


@optional
class IWireDefectTypesUpdate(WireDefectTypesBase):
    pass
