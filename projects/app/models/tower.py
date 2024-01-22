from datetime import datetime

from sqlmodel import Field, Relationship
from uuid import UUID
from typing import Optional
from sqlmodel import SQLModel

from app.models.base_uuid import BaseEntityModel


class BaseTower(SQLModel):
    name: str
    subproject_id: UUID = Field(foreign_key="Subproject.id")
    object_id: UUID = Field(nullable=False)
    status_id: UUID | None = Field(foreign_key="ObjectStatus.id", nullable=True) #todo cascade orphan? delete?


class TowerEntity(BaseTower, BaseEntityModel, table=True):

    __tablename__ = "TowerEntity"

    subproject: Optional["Subproject"] = Relationship(
        back_populates="towers_entities",
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "TowerEntity.subproject_id==Subproject.id"
        }
    )

    status: Optional["ObjectStatus"] = Relationship(
        back_populates="towers_entities",
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "TowerEntity.status_id==ObjectStatus.id"
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
