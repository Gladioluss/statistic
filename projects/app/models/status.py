from sqlmodel import Relationship

from app.models.base_uuid import BaseEntityModel
from sqlmodel import SQLModel
from uuid import UUID

class BaseProjectStatus(SQLModel):
    name: str

class BaseObjectStatus(SQLModel):
    name: str

class ProjectStatus(BaseProjectStatus, BaseEntityModel, table=True):

    __tablename__ = "ProjectStatus"

    projects: list["Project"] = Relationship(
        back_populates='status',
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "Project.status_id",
        }
    )

    subprojects: list["Subproject"] = Relationship(
        back_populates="status",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "Subproject.status_id",
        }
    )


class ObjectStatus(BaseObjectStatus, BaseEntityModel, table=True):

    __tablename__ = "ObjectStatus"

    spans_entities: list["SpanEntity"] = Relationship(
        back_populates="status",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "SpanEntity.status_id",
        }
    )

    towers_entities: list["TowerEntity"] = Relationship(
        back_populates="status",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "TowerEntity.status_id",
        }
    )