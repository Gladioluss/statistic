from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel
from app.models.string_defect_types import StringDefectTypes


class StringDefectsHistoryBase(SQLModel):
    main_id: UUID | None
    defect_id: UUID = Field(
        default=None, foreign_key="StringDefectTypes.id"
    )
    string_id: UUID
    flight_id: UUID | None
    coordinates: str | None
    description: str | None
    photo: str | None


class StringDefectsHistory(BaseUUIDModel, StringDefectsHistoryBase, table=True):
    string_defect_types: StringDefectTypes = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "StringDefectsHistory.defect_id==StringDefectTypes.id",
        }
    )
