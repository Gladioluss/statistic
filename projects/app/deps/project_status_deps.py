from app import crud
from app.models.status import ProjectStatus
from app.utils.exceptions.common import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated

async def get_project_status_by_name_from_path(
        name: Annotated[
            str, Path(description="String compare with name")
        ]
) -> ProjectStatus:
    project_status = await crud.project_status.get_by_name(name=name)
    if not project_status:
        raise NameNotFoundException(ProjectStatus, name=name)
    return project_status

async def get_project_status_by_id_from_path(
        id: Annotated[UUID, Path(description="The UUID id of the project status")]
) -> ProjectStatus:
    project_status = await crud.project_status.get(id=id)
    if not project_status:
        raise IdNotFoundException(ProjectStatus, id=id)
    return project_status

async def get_project_status_by_id_from_query(
        id: Annotated[UUID, Query(description="The UUID id of the project status")]
) -> ProjectStatus:
    project_status = await crud.project_status.get(id=id)
    if not project_status:
        raise IdNotFoundException(ProjectStatus, id=id)
    return project_status