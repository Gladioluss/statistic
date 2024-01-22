from uuid import UUID

from app import crud
from app.utils.exceptions.common import NameExistException, IdNotFoundException
from app.models.status import ObjectStatus


async def object_status_name_is_taken(name: str) -> None:
    obj = await crud.object_status.get_by_name(name=name)
    if obj:
        raise NameExistException(model=ObjectStatus, name=name)


async def object_status_is_exist(id: UUID) -> None:
    obj = await crud.object_status.get(id=id)
    if not obj:
        raise IdNotFoundException(model=ObjectStatus, id=id)