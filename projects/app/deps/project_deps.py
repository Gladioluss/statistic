from app import crud
from app.models.project import Project
from app.utils.exceptions.common import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_project_by_id_from_path(
        id: Annotated[UUID, Path(description="The UUID id of the project")]
) -> Project:
    project = await crud.project.get(id=id)
    if not project:
        raise IdNotFoundException(Project, id=id)
    return project


async def get_project_by_id_from_query(
        id: Annotated[UUID, Query(description="The UUID id of the project")]
) -> Project:
    project = await crud.project.get(id=id)
    if not project:
        raise IdNotFoundException(Project, id=id)
    return project