from app.crud.base import CRUDBase
from app.models.progress import Progress
from app.schemas.progress_schema import IProgressCreate, IProgressUpdate


class CRUDProgress(CRUDBase[Progress, IProgressCreate, IProgressUpdate]):
    pass


progress = CRUDProgress(Progress)
