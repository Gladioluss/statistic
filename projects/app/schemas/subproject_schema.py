from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime

from app.models.subproject import BaseSubproject
from app.utils.partial import optional
from app.models.project import Project
from app.models.status import ProjectStatus
from app.models.work_type import WorkType
from app.schemas.tower_schema import ITowerWithoutSubprojectId
from app.schemas.span_schema import ISpanWithoutSubprojectId

class ISubprojectCreate(BaseSubproject):
    pass
@optional
class ISubprojectUpdate(BaseSubproject):
    pass

class ISubprojectRead(BaseSubproject):
    id: UUID

class ISubprojectWithoutWorkTypeId(SQLModel):
    id: UUID
    name: str
    pl_segment_id: UUID
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    towers: list[UUID] | None = []
    spans: list[UUID] | None = []
    workers: UUID | None = None
    project_id: UUID
    status_id: UUID | None #todo none везде

class ISubprojectWithWorkTypeRead(ISubprojectWithoutWorkTypeId):
    work_type: WorkType

class ISubprojectWithoutProjectId(SQLModel):
    id: UUID
    name: str
    pl_segment_id: UUID
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    towers: list[UUID] | None = []
    spans: list[UUID] | None = []
    workers: UUID | None = None
    work_type_id: UUID
    status_id: UUID

class ISubprojectWithoutStatusId(SQLModel):
    id: UUID
    name: str
    pl_segment_id: UUID
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    towers: list[UUID] | None = []
    spans: list[UUID] | None = []
    workers: UUID | None = None
    work_type_id: UUID
    project_id: UUID

class ISubprojectWithStatusRead(ISubprojectWithoutStatusId):
    status: ProjectStatus

class ISubprojectWithProjectRead(ISubprojectWithoutProjectId):
    project: Project

class ISubprojectFullInfoRead(SQLModel):
    id: UUID
    name: str
    pl_segment_id: UUID
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    workers: UUID | None = None
    project: Project
    work_type: WorkType
    status: ProjectStatus
    towers: list[ITowerWithoutSubprojectId] | None = []
    spans: list[ISpanWithoutSubprojectId] | None = []