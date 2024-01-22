from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel


class StringDefectTypesBase(SQLModel):

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


class StringDefectTypes(BaseUUIDModel, StringDefectTypesBase, table=True):
    string_defects: list["StringDefects"] = Relationship(
        back_populates="string_defect_types",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    string_defects_history: list["StringDefectsHistory"] = Relationship(
        back_populates="string_defect_types",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
