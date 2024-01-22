from datetime import datetime

from sqlmodel import Field, Column, Relationship
from sqlalchemy import JSON
from typing import Optional
from uuid import UUID
from app.models.base_uuid import BaseEntityModel
from sqlmodel import SQLModel

class BaseSpan(SQLModel):
    name: str
    subproject_id: UUID = Field(foreign_key="Subproject.id")
    object_id: UUID = Field(nullable=False)
    wires: dict = Field(sa_column=Column(JSON), default={})
    status_id: UUID | None = Field(foreign_key="ObjectStatus.id", nullable=True)

class SpanEntity(BaseSpan, BaseEntityModel, table=True):

    __tablename__ = "SpanEntity"

    subproject: Optional["Subproject"] = Relationship(
        back_populates="spans_entities",
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "SpanEntity.subproject_id==Subproject.id"
        }
    )

    status: Optional["ObjectStatus"] = Relationship(
        back_populates="spans_entities",
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "SpanEntity.status_id==ObjectStatus.id"
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
