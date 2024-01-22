from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel

from app.models.project import BaseProject
from app.schemas.subproject_schema import ISubprojectWithoutProjectId, ISubprojectFullInfoRead
from app.utils.partial import optional
from app.models.status import ProjectStatus

class IProjectCreate(BaseProject): #todo optional
    pass

@optional
class IProjectUpdate(BaseProject):
    pass

class IProjectRead(BaseProject):
    id: UUID

class IProjectWithoutStatusId(SQLModel):
    id: UUID
    name: str
    order_number: str
    curator_id: UUID | None
    creator_id: UUID | None
    customer_id: UUID | None
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    admin_id: UUID | None

class IProjectWithStatus(SQLModel):
    id: UUID
    name: str
    order_number: str
    curator_id: UUID | None
    creator_id: UUID | None
    customer_id: UUID | None
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    admin_id: UUID | None
    status: ProjectStatus | None

class IProjectWithSubprojectsListRead(BaseProject):
    id: UUID
    subprojects: list[ISubprojectWithoutProjectId] | None = []

class IFullProjectInfoRead(SQLModel):
    id: UUID
    name: str
    order_number: str
    curator_id: UUID | None
    creator_id: UUID | None
    customer_id: UUID | None
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    admin_id: UUID | None
    status: ProjectStatus | None
    subprojects: list[ISubprojectWithoutProjectId] | None = []



