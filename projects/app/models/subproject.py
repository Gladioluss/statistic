from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from sqlalchemy import Column

from sqlalchemy.dialects import postgresql
from app.models.base_uuid import BaseEntityModel


class BaseSubproject(SQLModel):
    name: str
    pl_segment_id: UUID
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    workers: UUID | None = None
    work_type_id: UUID | None = Field(foreign_key="WorkType.id", nullable=True)
    project_id: UUID = Field(foreign_key="Project.id")
    status_id: UUID | None = Field(foreign_key="ProjectStatus.id", nullable=True)

class Subproject(BaseSubproject, BaseEntityModel, table=True):

    __tablename__ = "Subproject"

    project: Optional["Project"] = Relationship(
        back_populates='subprojects',
        sa_relationship_kwargs={
            "lazy": "joined",
            'primaryjoin': 'Subproject.project_id==Project.id'
        }
    )

    work_type: Optional["WorkType"] = Relationship(
        back_populates="subprojects",
        sa_relationship_kwargs={
            "lazy": "joined",
            'primaryjoin': 'Subproject.work_type_id==WorkType.id'
        }
    )

    status: Optional["ProjectStatus"] = Relationship(
        back_populates="subprojects",
        sa_relationship_kwargs={
            "lazy": "joined",
            'primaryjoin': 'Subproject.status_id==ProjectStatus.id'
        }
    )

    towers_entities: list["TowerEntity"] = Relationship(
        back_populates="subproject",
        sa_relationship_kwargs={
            "lazy": "selectin",
            'foreign_keys': 'TowerEntity.subproject_id',
            'cascade': 'all, delete-orphan'
        }
    )

    spans_entities: list["SpanEntity"] = Relationship(
        back_populates="subproject",
        sa_relationship_kwargs={
            "lazy": "selectin",
            'foreign_keys': 'SpanEntity.subproject_id',
            'cascade': 'all, delete-orphan'
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

