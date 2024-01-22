from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel


class TrackDefectTypesBase(SQLModel):
    name: str = Field(
        nullable=False, unique=True
    )
    eng_name: str = Field(
        nullable=False, unique=True
    )
    description: str | None


class TrackDefectTypes(BaseUUIDModel, TrackDefectTypesBase, table=True):
    track_defects: list["TrackDefects"] = Relationship(
        back_populates="track_defect_types",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
