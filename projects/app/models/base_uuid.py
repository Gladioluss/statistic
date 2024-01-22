from typing import Any

from sqlalchemy import inspect

from app.utils.uuid import uuid7, UUID
from sqlmodel import SQLModel as _SQLModel, Field
from sqlalchemy.orm import declared_attr
from datetime import datetime

class SQLModel(_SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

class BaseEntityModel(SQLModel):
    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )

    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    created_at: datetime | None = Field(default_factory=datetime.utcnow)



