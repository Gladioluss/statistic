from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_entity_model import BaseEntityModel


def current_year() -> int:
    return datetime.utcnow().year


def current_month() -> int:
    return datetime.utcnow().month


def current_day_of_week() -> int:
    return datetime.utcnow().weekday() + 1


def current_day_of_month() -> int:
    return datetime.utcnow().day


def current_quarter() -> int:
    month = datetime.utcnow().month
    return (month - 1) // 3 + 1


class BaseTime(SQLModel):
    day_of_month: int = Field(
        default_factory=current_day_of_month
    )
    month: int = Field(
        default_factory=current_month
    )
    quarter: int = Field(
        default_factory=current_quarter
    )
    year: int = Field(
        default_factory=current_year
    )
    day_of_week: int = Field(
        default_factory=current_day_of_week
    )


class Time(BaseTime, BaseEntityModel, table=True):

    progresses: list["Progress"] = Relationship(
        back_populates="time",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
