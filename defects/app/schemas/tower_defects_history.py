from uuid import UUID

from app.models.tower_defects_history import TowerDefectsHistoryBase
from app.utils.partial import optional


class ITowerDefectsHistoryCreate(TowerDefectsHistoryBase):
    pass


class ITowerDefectsHistoryRead(TowerDefectsHistoryBase):
    id: UUID


@optional
class ITowerDefectsHistoryUpdate(TowerDefectsHistoryBase):
    pass
