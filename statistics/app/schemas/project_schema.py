from uuid import UUID

from app.models.projects import BaseProject
from app.schemas.subproject_schema import ISubprojectWithoutProjectId
from app.utils.partial import optional


class IProjectRead(BaseProject):
    id: UUID


class IProjectCreate(BaseProject):
    pass


@optional
class IProjectUpdate(BaseProject):
    pass

class IProjectProgressInfoRead(BaseProject):
    id: UUID
    # calculated_completion_percentage: float | None = Field(alias='calculated_completion_percentage')


class IFullProjectInfoRead(BaseProject):
    id: UUID
    completion_percentage: float | None
    subprojects: list[ISubprojectWithoutProjectId] | None = []
