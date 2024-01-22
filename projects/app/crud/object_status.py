from app.crud.base import CRUDBase
from app.schemas.object_status_schema import IObjectStatusCreate, IObjectStatusUpdate
from app.models.status import ObjectStatus

class CRUDObjectStatus(CRUDBase[ObjectStatus, IObjectStatusCreate, IObjectStatusUpdate]):
    pass

object_status = CRUDObjectStatus(ObjectStatus)