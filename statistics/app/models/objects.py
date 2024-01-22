from enum import Enum
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.core.config import settings
from app.models.base_entity_model import BaseEntityModel
from app.models.subprojects import Subproject


class ObjectType(str, Enum):
    TOWER = "TowerEntity"
    SPAN = "SpanEntity"


class ObjectStatus(str, Enum):
    READY = settings.OBJECT_AVAILABILITY_STATUS
    NOT_READY = "Не готово"


class BaseObject(SQLModel):
    real_object_id: UUID
    object_type: ObjectType
    subproject_id: UUID = Field(foreign_key="Subproject.id")
    status: str


class Object(BaseObject, BaseEntityModel, table=True):


    subproject: Subproject = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Object.subproject_id==Subproject.id",
        }
    )

    progresses: list["Progress"] | None = Relationship(
        back_populates="object",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    defects: list["Defect"] = Relationship(
        back_populates="object",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def defects_count(self) -> int:
        return len(self.defects)
