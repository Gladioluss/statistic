from uuid import UUID

from app import crud
from app.utils.exceptions.common import NameExistException, IdNotFoundException
from app.models.work_type import WorkType


async def work_type_name_is_taken(name: str) -> None:
    obj = await crud.work_type.get_by_name(name=name)
    if obj:
        raise NameExistException(model=WorkType, name=name)


async def work_type_is_exist(id: UUID) -> None:
    obj = await crud.work_type.get(id=id)
    if not obj:
        raise IdNotFoundException(model=WorkType, id=id)