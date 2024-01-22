from uuid import UUID

from app.models.defects import BaseDefect
from app.utils.partial import optional


class IDefectRead(BaseDefect):
    id: UUID


class IDefectCreate(BaseDefect):
    pass


@optional
class IDefectUpdate(BaseDefect):
    pass
