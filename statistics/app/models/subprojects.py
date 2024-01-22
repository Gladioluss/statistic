from math import floor
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.core.config import settings
from app.models.base_entity_model import BaseEntityModel
from app.models.projects import Project


class BaseSubproject(SQLModel):
    real_subproject_id: UUID
    name: str
    project_id: UUID = Field(foreign_key="Project.id")


class Subproject(BaseSubproject, BaseEntityModel, table=True):
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Subproject.project_id==Project.id",
        }
    )

    objects: list["Object"] | None = Relationship(
        back_populates="subproject",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def count_objects(self) -> int:
        return len(self.objects)


    @property
    def completion_percentage(self) -> float:
        total_objects = len(self.objects)
        completed_objects = len(
            [obj for obj in self.objects if obj.status == settings.OBJECT_AVAILABILITY_STATUS]
        )

        if total_objects > 0:
            multiplier = 10 ** 2
            value = (completed_objects / total_objects) * 100
            return floor(value * multiplier + 0.5) / multiplier
        else:
            return 0.0

