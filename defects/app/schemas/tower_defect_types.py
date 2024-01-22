from uuid import UUID

from app.models.tower_defect_types import TowerDefectTypesBase
from app.utils.partial import optional


class ITowerDefectTypesCreate(TowerDefectTypesBase):
    pass


class ITowerDefectTypesRead(TowerDefectTypesBase):
    id: UUID


@optional
class ITowerDefectTypesUpdate(TowerDefectTypesBase):
    pass
