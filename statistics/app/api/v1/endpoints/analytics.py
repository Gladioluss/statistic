from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params

from app import crud
from app.deps import object_deps, project_deps
from app.models import Object, Project
from app.schemas.object_schema import IObjectFullInfo, IObjectRead, IObjectWithoutSubprojectId
from app.schemas.project_schema import IFullProjectInfoRead, IProjectRead
from app.schemas.response_schema import IGetResponseBase, IGetResponsePaginated, create_response
from app.schemas.subproject_schema import ISubprojectRead

router = APIRouter()


@router.get("/project/list")
async def _get_all_projects_paginated(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IProjectRead]:
    """
    Get a paginated list of projects
    """
    projects = await crud.project.get_multi_paginated_without_subproject(params=params)
    return create_response(data=projects)


@router.get("/subproject/list")
async def _get_all_subprojects_paginated(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[ISubprojectRead]:
    """
    Get a paginated list of subprojects
    """
    subprojects = await crud.subproject.get_multi_paginated_without_object(params=params)
    return create_response(data=subprojects)


@router.get("/object/list")
async def _get_all_objects_paginated(
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IObjectRead]:
    """
    Get a paginated list of objects
    """
    objects = await crud.object.get_multi_paginated(params=params)
    return create_response(data=objects)


@router.get("/project/{project_id}/progress")
async def _get_project_progress(
        project: Project = Depends(project_deps.get_project_by_id_from_path)  # noqa: B008
) -> IGetResponseBase[IFullProjectInfoRead]:
    """
    Get the project and its subprojects with execution progress
    """
    return create_response(data=project)


@router.get("/project/{project_id}/progress/date/{selected_date}")
async def _get_project_progress_info_by_date(
        project: Project = Depends(project_deps.get_project_by_date_from_path)  # noqa: B008
) -> IGetResponseBase[IFullProjectInfoRead]:
    """
    Get a project with progress up to the entered date
    """
    return create_response(data=project)


@router.get("/project/{project_id}/progress/year/{year}")
async def _get_project_progress_info_by_year(
        project: Project = Depends(project_deps.get_project_by_year_from_path)  # noqa: B008
) -> IGetResponseBase[IFullProjectInfoRead]:
    """
    Get a project with progress up to the entered year
    """
    return create_response(data=project)


@router.get("/project/{project_id}/progress/quarter")
async def _get_project_progress_info_by_quarter(
        project: Project = Depends(             # noqa: B008
            project_deps.get_project_by_quarter
        )
) -> IGetResponseBase[IFullProjectInfoRead]:
    """
    Get a project with progress up to the entered quarter
    """
    return create_response(data=project)


@router.get("/subproject/{subproject_id}/objects")
async def _get_objects_by_subproject_id_paginated(
        subproject_id: UUID,
        params: Params = Depends()  # noqa: B008
) -> IGetResponsePaginated[IObjectRead]:
    """
    Get a paginated list of objects in a subproject
    """
    objects = await crud.object.get_multi_by_subproject_id_paginated(
        subproject_id=subproject_id,
        params=params
    )
    return create_response(data=objects)


@router.get("/object/{object_id}/info")
async def _get_object_full_info(
    object: Object = Depends(object_deps.get_object_by_id_from_path)  # noqa: B008
) -> IGetResponseBase[IObjectWithoutSubprojectId]:
    """
    Get an object with progress information
    """
    return create_response(data=object)


@router.get("/object/{id}/defects")
async def _get_object_defects_info(
    object: Object = Depends(object_deps.get_object_by_id_from_path)  # noqa: B008
) -> IGetResponseBase[IObjectFullInfo]:
    """
    Get an object with defects
    """
    return create_response(data=object)
