from uuid import UUID
from sqlmodel import SQLModel

from app.models.status import ObjectStatus
from app.models.subproject import Subproject
from app.models.span import BaseSpan
from app.utils.partial import optional


class ISpanCreate(BaseSpan):
    pass


@optional
class ISpanUpdate(BaseSpan):
    pass


class ISpanRead(BaseSpan):
    id: UUID


class ISpanWithoutObjectStatusId(SQLModel):
    id: UUID
    name: str
    subproject_id: UUID
    wires: dict | None = None


class ISpanWithObjectStatusRead(ISpanWithoutObjectStatusId):
    status: ObjectStatus | None = None


class ISpanWithoutSubprojectId(SQLModel):
    id: UUID
    name: str
    wires: dict | None = None
    status_id: UUID | None = None


class ISpanWithSubprojectRead(SQLModel):
    subproject: Subproject


class ISpanWithFullInfoRead(SQLModel):
    id: UUID
    name: str
    wires: dict | None = None
    status: ObjectStatus | None = None
    subproject: Subproject



