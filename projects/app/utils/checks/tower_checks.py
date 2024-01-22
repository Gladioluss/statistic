from uuid import UUID

from app import crud
from app.utils.exceptions.common import NameExistException, IdNotFoundException
from app.models.tower import TowerEntity


async def tower_name_is_taken_in_current_subproject(name: str, subproject_id: UUID) -> None:
    obj = await crud.tower.get_by_name_in_current_subproject(name=name, subproject_id=subproject_id)
    if obj:
        raise NameExistException(model=TowerEntity, name=name)


async def tower_is_exist(id: UUID) -> None:
    obj = await crud.tower.get(id=id)
    if not obj:
        raise IdNotFoundException(model=TowerEntity, id=id)