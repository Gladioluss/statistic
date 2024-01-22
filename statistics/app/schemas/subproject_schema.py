from uuid import UUID

from sqlmodel import SQLModel

from app.models.subprojects import BaseSubproject
from app.utils.partial import optional


class ISubprojectRead(BaseSubproject):
    id: UUID


class ISubprojectCreate(BaseSubproject):
    pass


@optional
class ISubprojectUpdate(BaseSubproject):
    pass

class ISubprojectWithoutProjectId(SQLModel):
    real_subproject_id: UUID
    name: str
    completion_percentage: float | None
    id: UUID
    count_objects: int | None
    # objects: list[IObjectWithoutSubprojectId] | None = []
