from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel
from app.models.track_defect_types import TrackDefectTypes


class TrackDefectsBase(SQLModel):
    defect_id: UUID = Field(
        default=None, foreign_key="TrackDefectTypes.id"
    )
    span_id: UUID
    flight_id: UUID
    coordinates: str | None
    description: str | None
    photo: str | None


class TrackDefects(BaseUUIDModel, TrackDefectsBase, table=True):
    track_defect_types: TrackDefectTypes = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "TrackDefects.defect_id==TrackDefectTypes.id",
        }
    )
