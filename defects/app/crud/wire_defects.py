from typing import TypeVar

from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models import WireDefects
from app.schemas.wire_defects import IWireDefectsCreate, IWireDefectsUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDWireDefects(
    CRUDBase[
        WireDefects,
        IWireDefectsCreate,
        IWireDefectsUpdate
    ]
):
    pass


wire_defects = CRUDWireDefects(WireDefects)
