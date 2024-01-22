from typing import TypeVar

from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models import StringDefectTypes
from app.schemas.string_defect_types import IStringDefectTypesCreate, IStringDefectTypesUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDStringDefectTypes(
    CRUDBase[
        StringDefectTypes,
        IStringDefectTypesCreate,
        IStringDefectTypesUpdate
    ]
):
    pass


string_defect_types = CRUDStringDefectTypes(StringDefectTypes)
