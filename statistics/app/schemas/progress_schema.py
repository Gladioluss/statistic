from uuid import UUID

from sqlmodel import SQLModel

from app.models.progress import ProgressBase
from app.schemas.time_schema import ITimeRead
from app.utils.partial import optional


class IProgressRead(ProgressBase):
    id: UUID


class IProgressCreate(ProgressBase):
    pass


@optional
class IProgressUpdate(ProgressBase):
    pass

class IProgressWithoutObjectId(SQLModel):
    progress: bool
    id: UUID
    time: ITimeRead
