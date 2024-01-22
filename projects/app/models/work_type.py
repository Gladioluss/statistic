from sqlmodel import Relationship
from sqlmodel import SQLModel

from app.models.base_uuid import BaseEntityModel

class BaseWorkType(SQLModel):
    name: str

class WorkType(BaseEntityModel, BaseWorkType, table=True):

    __tablename__ = "WorkType"

    subprojects: list["Subproject"] = Relationship(
        back_populates="work_type",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "Subproject.work_type_id",
            "cascade": "all"
        }
    )