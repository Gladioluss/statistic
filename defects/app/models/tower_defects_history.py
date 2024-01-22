from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel
from app.models.tower_defect_types import TowerDefectTypes


class TowerDefectsHistoryBase(SQLModel):
    main_id: UUID | None
    defect_id: UUID = Field(
        default=None, foreign_key="TowerDefectTypes.id"
    )
    tower_id: UUID
    flight_id: UUID | None
    coordinates: str | None
    description: str | None
    photo: str | None


class TowerDefectsHistory(BaseUUIDModel, TowerDefectsHistoryBase, table=True):
    tower_defect_types: TowerDefectTypes = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "TowerDefectsHistory.defect_id==TowerDefectTypes.id",
        }
    )
