

from app.crud.base import CRUDBase
from app.schemas.work_type_schema import IWorkTypeCreate, IWorkTypeUpdate
from app.models.work_type import WorkType


class CRUDWorkType(CRUDBase[WorkType, IWorkTypeCreate, IWorkTypeUpdate]):
    pass

work_type = CRUDWorkType(WorkType)