from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid import BaseUUIDModel


class TowerDefectTypesBase(SQLModel):
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


class TowerDefectTypes(BaseUUIDModel, TowerDefectTypesBase, table=True):
    tower_defects: list["TowerDefects"] = Relationship(
        back_populates="tower_defect_types",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    tower_defects_history: list["TowerDefectsHistory"] = Relationship(
        back_populates="tower_defect_types",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
