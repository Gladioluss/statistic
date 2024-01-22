from uuid import UUID

from app.models.tower_defects import TowerDefectsBase
from app.utils.partial import optional


class ITowerDefectsCreate(TowerDefectsBase):
    pass


class ITowerDefectsRead(TowerDefectsBase):
    id: UUID


@optional
class ITowerDefectsUpdate(TowerDefectsBase):
    pass

