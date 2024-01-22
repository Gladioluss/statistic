from sqlmodel import Field, Relationship
from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel

from app.models.base_uuid import BaseEntityModel

class BaseProject(SQLModel):
    name: str
    order_number: str
    curator_id: UUID | None
    creator_id: UUID | None
    customer_id: UUID | None
    start_date_planned: datetime | None
    complete_date_planned: datetime | None
    start_date_real: datetime | None
    complete_date_real: datetime | None
    admin_id: UUID | None
    status_id: UUID | None = Field(foreign_key="ProjectStatus.id", nullable=True)

class Project(BaseProject, BaseEntityModel, table=True):

    __tablename__ = "Project"

    status: Optional["ProjectStatus"] = Relationship(
        back_populates='projects',
        sa_relationship_kwargs={
            "lazy": "joined",
            'primaryjoin': 'Project.status_id==ProjectStatus.id'
        }
    )
    subprojects: list["Subproject"] = Relationship(
        back_populates='project',
        sa_relationship_kwargs = {
            "lazy": "selectin",
            'foreign_keys': 'Subproject.project_id',
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
