from typing import TypeVar

from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models import TrackDefects
from app.schemas.track_defects import ITrackDefectsCreate, ITrackDefectsUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDTrackDefects(
    CRUDBase[
        TrackDefects,
        ITrackDefectsCreate,
        ITrackDefectsUpdate
    ]
):
    pass


track_defects = CRUDTrackDefects(TrackDefects)
