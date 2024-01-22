from typing import TypeVar

from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models import WireDefectTypes
from app.schemas.wire_defect_types import IWireDefectTypesCreate, IWireDefectTypesUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDWireDefectTypes(
    CRUDBase[
        WireDefectTypes,
        IWireDefectTypesCreate,
        IWireDefectTypesUpdate
    ]
):
    pass


wire_defect_types = CRUDWireDefectTypes(WireDefectTypes)
