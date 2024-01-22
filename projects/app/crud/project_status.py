

from app.crud.base import CRUDBase
from app.schemas.project_status_schema import IProjectStatusCreate, IProjectStatusUpdate
from app.models.status import ProjectStatus


class CRUDProjectStatus(CRUDBase[ProjectStatus, IProjectStatusCreate, IProjectStatusUpdate]):
    pass

project_status = CRUDProjectStatus(ProjectStatus)