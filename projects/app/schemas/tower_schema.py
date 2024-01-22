from uuid import UUID
from sqlmodel import SQLModel

from app.models.tower import BaseTower
from app.utils.partial import optional
from app.models.status import ObjectStatus
from app.models.subproject import Subproject


class ITowerCreate(BaseTower):
    pass


@optional
class ITowerUpdate(BaseTower):
    pass


class ITowerRead(BaseTower):
    id: UUID


class ITowerWithoutObjectStatusId(SQLModel):
    id: UUID
    name: str
    subproject_id: UUID


class ITowerWithObjectStatusRead(ITowerWithoutObjectStatusId):
    status: ObjectStatus | None = None


class ITowerWithoutSubprojectId(SQLModel):
    id: UUID
    name: str
    object_id: UUID
    status_id: UUID | None = None


class ITowerWithSubprojectRead(ITowerWithoutSubprojectId):
    subproject: Subproject


class ITowerFullInfoRead(SQLModel):
    id: UUID
    name: str
    status: ObjectStatus | None = None
    subproject: Subproject
    object_id: UUID




