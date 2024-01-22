from uuid import UUID

from app.models.work_type import BaseWorkType
from app.utils.partial import optional
from app.models.subproject import Subproject

class IWorkTypeCreate(BaseWorkType):
    pass

@optional
class IWorkTypeUpdate(BaseWorkType):
    pass

class IWorkTypeRead(BaseWorkType):
     id: UUID

class IWorkTypeWithSubprojectsRead(BaseWorkType):
    id: UUID
    subprojects: list[Subproject] | None = []