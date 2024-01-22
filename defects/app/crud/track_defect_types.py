from typing import TypeVar

from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models import TrackDefectTypes
from app.schemas.track_defect_types import ITrackDefectTypesCreate, ITrackDefectTypesUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDTrackDefectTypes(
    CRUDBase[
        TrackDefectTypes,
        ITrackDefectTypesCreate,
        ITrackDefectTypesUpdate
    ]
):
    pass


track_defect_types = CRUDTrackDefectTypes(TrackDefectTypes)
