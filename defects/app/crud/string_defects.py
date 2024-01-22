from typing import TypeVar

from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models import StringDefects
from app.schemas.string_defects import IStringDefectsCreate, IStringDefectsUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDStringDefects(
    CRUDBase[
        StringDefects,
        IStringDefectsCreate,
        IStringDefectsUpdate
    ]
):
    pass


string_defects = CRUDStringDefects(StringDefects)
