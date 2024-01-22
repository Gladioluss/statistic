from uuid import UUID

from app import crud
from app.utils.exceptions.common import NameExistException, IdNotFoundException
from app.models.span import SpanEntity


async def span_name_is_taken_in_current_subproject(name: str, subproject_id: UUID) -> None:
    obj = await crud.span.get_by_name_in_current_subproject(name=name, subproject_id=subproject_id)
    if obj:
        raise NameExistException(model=SpanEntity, name=name)


async def span_is_exist(id: UUID) -> None:
    obj = await crud.span.get(id=id)
    if not obj:
        raise IdNotFoundException(model=SpanEntity, id=id)