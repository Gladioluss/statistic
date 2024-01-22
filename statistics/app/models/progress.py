from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_entity_model import BaseEntityModel
from app.models.objects import Object
from app.models.times import Time


class ProgressBase(SQLModel):
    time_id: UUID = Field(foreign_key="Time.id")
    object_id: UUID = Field(foreign_key="Object.id")
    progress: bool


class Progress(ProgressBase, BaseEntityModel, table=True):


    object: Object = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Progress.object_id==Object.id",
        }
    )

    time: Time = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Progress.time_id==Time.id",
        }
    )


