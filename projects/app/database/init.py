from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from .base_data import *

async def insert_base_data(db_session: AsyncSession) -> None:
    for work_type in work_types:
        work_type_current = await crud.work_type.get_by_name(
            name=work_type.name, db_session=db_session
        )
        if not work_type_current:
            await crud.work_type.create(obj_in=work_type, db_session=db_session)

    for project_status in project_statuses:
        project_status_current = await crud.project_status.get_by_name(
            name=project_status.name, db_session=db_session
        )
        if not project_status_current:
            await crud.project_status.create(obj_in=project_status, db_session=db_session)

    for object_status in object_statuses:
        object_status_current = await crud.object_status.get_by_name(
            name=object_status.name, db_session=db_session
        )
        if not object_status_current:
            await crud.object_status.create(obj_in=object_status, db_session=db_session)