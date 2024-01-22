from uuid import UUID

from app import crud
from app.utils.exceptions.common import NameExistException, IdNotFoundException
from app.models.subproject import Subproject


async def subproject_name_is_taken_in_current_project(name: str, project_id: UUID) -> None:
    obj = await crud.subproject.get_by_name_in_current_project(name=name, project_id=project_id)
    if obj:
        raise NameExistException(model=Subproject, name=name)


async def subproject_is_exist(id: UUID) -> None:
    obj = await crud.subproject.get(id=id)
    if not obj:
        raise IdNotFoundException(model=Subproject, id=id)