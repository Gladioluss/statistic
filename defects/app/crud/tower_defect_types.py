from typing import TypeVar

from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models import TowerDefectTypes
from app.schemas.tower_defect_types import ITowerDefectTypesCreate, ITowerDefectTypesUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDTowerDefectTypes(
    CRUDBase[
        TowerDefectTypes,
        ITowerDefectTypesCreate,
        ITowerDefectTypesUpdate
    ]
):
    pass


tower_defect_types = CRUDTowerDefectTypes(TowerDefectTypes)
