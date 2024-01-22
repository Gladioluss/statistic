from math import floor
from uuid import UUID

from sqlmodel import Relationship, SQLModel

from app.core.config import settings
from app.models.base_entity_model import BaseEntityModel


class BaseProject(SQLModel):
    real_project_id: UUID
    name: str


class Project(BaseProject, BaseEntityModel, table=True):

    subprojects: list["Subproject"] | None = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def completion_percentage(self) -> float:
        total_objects = sum(len(subproject.objects) for subproject in self.subprojects)
        completed_objects = (
            sum(
                len(
                    [obj for obj in subproject.objects if obj.status == settings.OBJECT_AVAILABILITY_STATUS]
                )
                for subproject in self.subprojects)
        )

        if total_objects > 0:
            multiplier = 10 ** 2
            value = (completed_objects / total_objects) * 100
            return floor(value * multiplier + 0.5) / multiplier
        else:
            return 0.0

