from uuid import UUID

from app import crud
from app.utils.exceptions.common import NameExistException, IdNotFoundException
from app.models.project import Project


async def project_name_is_taken(name: str) -> None:
    obj = await crud.project.get_by_name(name=name)
    if obj:
        raise NameExistException(model=Project, name=name)


async def project_is_exist(id: UUID) -> None:
    obj = await crud.project.get(id=id)
    if not obj:
        raise IdNotFoundException(model=Project, id=id)