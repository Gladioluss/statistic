from uuid import UUID

from app.models.string_defects_history import StringDefectsHistoryBase
from app.utils.partial import optional


class IStringDefectsHistoryCreate(StringDefectsHistoryBase):
    pass


class IStringDefectsHistoryRead(StringDefectsHistoryBase):
    id: UUID


@optional
class IStringDefectsHistoryUpdate(StringDefectsHistoryBase):
    pass
