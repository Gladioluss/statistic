from uuid import UUID

from app.models.base_entity_model import SQLModel
from app.models.objects import BaseObject, ObjectType
from app.schemas.defect_schema import IDefectRead
from app.schemas.progress_schema import IProgressWithoutObjectId
from app.utils.partial import optional


class IObjectRead(BaseObject):
    id: UUID
    defects_count: int = 0


class IObjectCreate(BaseObject):
    pass


@optional
class IObjectUpdate(BaseObject):
    pass


class IObjectWithoutSubprojectId(SQLModel):
    real_object_id: UUID
    object_type: ObjectType
    status: str
    progresses: list[IProgressWithoutObjectId] | None = []


class IObjectFullInfo(BaseObject):
    id: UUID
    defects_count: int = 0
    defects : list[IDefectRead] | None = []
