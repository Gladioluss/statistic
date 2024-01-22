from uuid import UUID

from app import crud
from app.utils.exceptions.common import NameExistException, IdNotFoundException
from app.models.status import ProjectStatus


async def project_status_name_is_taken(name: str) -> None:
    obj = await crud.project_status.get_by_name(name=name)
    if obj:
        raise NameExistException(model=ProjectStatus, name=name)


async def project_status_is_exist(id: UUID) -> None:
    obj = await crud.project_status.get(id=id)
    if not obj:
        raise IdNotFoundException(model=ProjectStatus, id=id)