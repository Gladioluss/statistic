from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel
from app.models.wire_defect_types import WireDefectTypes


class WireDefectsHistoryBase(SQLModel):
    main_id: UUID | None
    defect_id: UUID = Field(
        default=None, foreign_key="WireDefectTypes.id"
    )
    wire_id: UUID
    flight_id: UUID | None
    coordinates: str | None
    description: str | None
    photo: str | None
    distance_from_tower_1: float | None
    distance_from_tower_2: float | None


class WireDefectsHistory(BaseUUIDModel, WireDefectsHistoryBase, table=True):
    wire_defect_types: WireDefectTypes = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "WireDefectsHistory.defect_id==WireDefectTypes.id",
        }
    )
