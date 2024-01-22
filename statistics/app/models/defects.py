from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_entity_model import BaseEntityModel
from app.models.objects import Object


class BaseDefect(SQLModel):
    object_id: UUID = Field(foreign_key="Object.id")
    defect_id: UUID
    defect_description: str


class Defect(BaseDefect, BaseEntityModel, table=True):

    object: Object = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Defect.object_id==Object.id",
        }
    )
