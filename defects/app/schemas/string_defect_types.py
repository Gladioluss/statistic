from uuid import UUID

from app.models.string_defect_types import StringDefectTypesBase
from app.utils.partial import optional


class IStringDefectTypesCreate(StringDefectTypesBase):
    pass


class IStringDefectTypesRead(StringDefectTypesBase):
    id: UUID


@optional
class IStringDefectTypesUpdate(StringDefectTypesBase):
    pass
