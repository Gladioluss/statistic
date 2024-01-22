from sqlmodel.ext.asyncio.session import AsyncSession
from uuid_extensions import uuid7
import random

from app.database.base_data import *
from app import crud
from app.schemas.project_schema import IProjectCreate
from app.schemas.tower_schema import ITowerCreate
from app.schemas.span_schema import ISpanCreate
from app.schemas.subproject_schema import ISubprojectCreate


async def insert_test_data(db_session: AsyncSession):
    for n, status in enumerate(project_statuses):
        status_current = await crud.project_status.get_by_name(
            name=status.name,
            db_session=db_session
        )

        project = IProjectCreate(
                name='Проект {}'.format(n),
                order_number='Договор {}'.format(n),
                status_id=status_current.id
        )

        project_current = await crud.project.get_by_name(
            name=project.name,
            db_session=db_session
        )

        if not project_current:
            await crud.project.create(
                obj_in=project,
                db_session=db_session
            )
            created_project = await crud.project.get_by_name(name=project.name, db_session=db_session)
            project_id=created_project.id

        else:
            project_id = project_current.id


        for i, work_type in enumerate(work_types):
            work_type_current = await crud.work_type.get_by_name(
                name=work_type.name,
                db_session=db_session
            )

            subproject = ISubprojectCreate(
                name='Подпроект {}{}'.format(n,i),
                project_id=project_id,
                pl_segment_id=uuid7(),
                work_type_id=work_type_current.id,
                status_id=status_current.id,
            )

            subproject_current = await crud.subproject.get_by_name(
                name=subproject.name,
                db_session=db_session
            )

            if not subproject_current:
                await crud.subproject.create(
                    obj_in=subproject,
                    db_session=db_session
                )
                created_subproject = await crud.subproject.get_by_name(name=subproject.name, db_session=db_session)
                subproject_id = created_subproject.id

            else: subproject_id = subproject_current.id

            for n_obj_status, obj_status in enumerate(object_statuses):
                obj_status_current = await crud.object_status.get_by_name(name=obj_status.name, db_session=db_session)

                tower = ITowerCreate (
                    name="Опора {}".format(random.randint(0, 1408)),
                    subproject_id=subproject_id,
                    object_id=uuid7(),
                    status_id=obj_status_current.id
                )
                span = ISpanCreate (
                    name="Пролет {}".format(random.randint(0, 1408)),
                    subproject_id=subproject_id,
                    object_id=uuid7(),
                    status_id=obj_status_current.id
                )

                await crud.tower.create(obj_in=tower, db_session=db_session)
                await crud.span.create(obj_in=span, db_session=db_session)