from uuid import UUID

from pydantic import BaseModel

from app.models.times import BaseTime
from app.utils.partial import optional


class ITimeRead(BaseTime):
    id: UUID


class ITimeCreate(BaseTime):
    pass


@optional
class ITimeUpdate(BaseTime):
    pass

class ITimeRequest(BaseModel):
    day_of_month: int
    month: int
    year: int
