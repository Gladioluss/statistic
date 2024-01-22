from uuid import UUID

from app.models.string_defects import StringDefectsBase
from app.utils.partial import optional


class IStringDefectsCreate(StringDefectsBase):
    pass


class IStringDefectsRead(StringDefectsBase):
    id: UUID


@optional
class IStringDefectsUpdate(StringDefectsBase):
    pass
