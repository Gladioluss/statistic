from uuid import UUID

from app.models.status import BaseObjectStatus
from app.utils.partial import optional
from app.schemas.span_schema import ISpanWithoutObjectStatusId
from app.schemas.tower_schema import ITowerWithoutObjectStatusId

class IObjectStatusCreate(BaseObjectStatus):
    pass

@optional
class IObjectStatusUpdate(BaseObjectStatus):
    pass

class IObjectStatusRead(BaseObjectStatus):
    id: UUID

class IObjectStatusWithAllObjectsListRead(BaseObjectStatus):
    id: UUID
    towers_entities: list[ITowerWithoutObjectStatusId] | None = []
    spans_entities: list[ISpanWithoutObjectStatusId] | None = []

class IObjectStatusWithTowersListRead(BaseObjectStatus):
    id: UUID
    towers_entities: list[ITowerWithoutObjectStatusId] | None = []

class IObjectStatusWithSpansListRead(BaseObjectStatus):
    id: UUID
    spans_entities: list[ISpanWithoutObjectStatusId] | None = []