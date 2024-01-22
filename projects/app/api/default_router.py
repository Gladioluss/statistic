from fastapi import APIRouter
from app.api.endpoints import (
    work_types,
    project_statuses,
    object_statuses,
    projects,
    subprojects,
    towers,
    spans
)

default_router = APIRouter()
default_router.include_router(work_types.router, prefix="/work_type", tags=["WorkType"])
default_router.include_router(project_statuses.router, prefix="/project_status", tags=["ProjectStatus"])
default_router.include_router(object_statuses.router, prefix="/object_status", tags=["ObjectStatus"])
default_router.include_router(projects.router, prefix="/project", tags=["Projects"])
default_router.include_router(subprojects.router, prefix="/subproject", tags=["Subprojects"])
default_router.include_router(towers.router, prefix="/tower", tags=["Towers"])
default_router.include_router(spans.router, prefix="/span", tags=["Spans"])