from uuid import UUID

from app.models.status import BaseProjectStatus
from app.utils.partial import optional
from app.schemas.project_schema import IProjectWithoutStatusId
from app.schemas.subproject_schema import ISubprojectWithoutStatusId

class IProjectStatusCreate(BaseProjectStatus):
    pass

@optional
class IProjectStatusUpdate(BaseProjectStatus):
    pass

class IProjectStatusRead(BaseProjectStatus):
    id: UUID

class IProjectStatusWithProjectsRead(BaseProjectStatus):
    id: UUID
    projects: list[IProjectWithoutStatusId] | None = []

class IProjectStatusWithSubrojectsRead(BaseProjectStatus):
    id: UUID
    subprojects: list[ISubprojectWithoutStatusId] | None = []

class IProjectStatusWithSubrojectsAndProjectsRead(BaseProjectStatus):
    id: UUID
    projects: list[IProjectWithoutStatusId] | None = []
    subprojects: list[ISubprojectWithoutStatusId] | None = []
