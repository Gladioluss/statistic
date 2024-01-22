from typing import TypeVar

from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models import TowerDefects
from app.schemas.tower_defects import ITowerDefectsCreate, ITowerDefectsUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDTowerDefects(
    CRUDBase[
        TowerDefects,
        ITowerDefectsCreate,
        ITowerDefectsUpdate
    ]
):
    pass


tower_defects = CRUDTowerDefects(TowerDefects)
