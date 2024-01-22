from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel
from app.models.tower_defect_types import TowerDefectTypes


class TowerDefectsBase(SQLModel):
    defect_id: UUID = Field(
        default=None, foreign_key="TowerDefectTypes.id"
    )
    tower_id: UUID
    flight_id: UUID | None
    coordinates: str | None
    description: str | None
    photo: str | None


class TowerDefects(BaseUUIDModel, TowerDefectsBase, table=True):

    tower_defect_types: TowerDefectTypes = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "TowerDefects.defect_id==TowerDefectTypes.id",
        }
    )

    @staticmethod
    def _serialize_item(item: UUID | datetime) -> str | None:
        if isinstance(item, UUID):
            return str(item)
        elif isinstance(item, datetime):
            return item.isoformat()
        return item

    def to_dict(self) -> dict:
        return {k: self._serialize_item(v) for k, v in super().dict().items()}

