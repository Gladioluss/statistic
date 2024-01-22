from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel


class WireDefectTypesBase(SQLModel):
    name: str = Field(
        nullable=False, unique=True
    )
    eng_name: str = Field(
        nullable=False, unique=True
    )
    description: str | None
    short_name: str = Field(
        nullable=True, unique=True
    )


class WireDefectTypes(BaseUUIDModel, WireDefectTypesBase, table=True):
    wire_defects: list["WireDefects"] = Relationship(
        back_populates="wire_defect_types",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    wire_defects_history: list["WireDefectsHistory"] = Relationship(
        back_populates="wire_defect_types",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
