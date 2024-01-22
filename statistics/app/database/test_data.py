from random import random
from uuid import UUID

from loguru import logger
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid_extensions import uuid7

from app import crud
from app.models.objects import ObjectStatus, ObjectType
from app.schemas.object_schema import IObjectCreate, IObjectUpdate
from app.schemas.progress_schema import IProgressCreate
from app.schemas.project_schema import IProjectCreate
from app.schemas.subproject_schema import ISubprojectCreate
from app.schemas.time_schema import ITimeCreate
from app.utils.checks.time_checks import check_time_exists


async def create_time(time: ITimeCreate, db_session: AsyncSession) -> UUID:
    time_check = await check_time_exists(
        time=time,
        db_session=db_session
    )
    if time_check is None:
        new_time = await crud.time.create(
            obj_in=time,
            db_session=db_session
        )
    else:
        new_time = time_check

    return new_time.id


async def insert_test_data(db_session: AsyncSession):
    time_2022_id = await create_time(
        time=ITimeCreate(
            day_of_month=10,
            month=9,
            quarter=3,
            year=2022,
            day_of_week=4,
        ),
        db_session=db_session
    )
    time_2023_id_first = await create_time(
        time=ITimeCreate(
            day_of_month=10,
            month=12,
            quarter=4,
            year=2023,
            day_of_week=4,
        ),
        db_session=db_session
    )
    time_2023_id = await create_time(
        time=ITimeCreate(),
        db_session=db_session
    )

    for p in range(0, 1):
        project = IProjectCreate(
            name=f'Проект 22{p}',
            real_project_id=uuid7()
        )

        current_project = await crud.project.create(
            obj_in=project,
            db_session=db_session
        )

        for s in range(0, 4):
            object = ISubprojectCreate(
                name=f'Подпроект {s}',
                project_id=current_project.id,
                real_subproject_id=uuid7(),
            )

            current_subproject = await crud.subproject.create(
                obj_in=object,
                db_session=db_session
            )

            for _o in range(0, 150):
                object = IObjectCreate(
                    object_type=ObjectType.SPAN,
                    subproject_id=current_subproject.id,
                    status=ObjectStatus.NOT_READY,
                    real_object_id=uuid7(),
                )

                current_object = await crud.object.create(
                    obj_in=object,
                    db_session=db_session
                )

                # logger.info(f"Object {current_object.id}")
                rand_value = random()
                if  rand_value< 0.37:
                    new_time = time_2022_id
                else:
                    new_time = time_2023_id

                await crud.progress.create(
                    obj_in=IProgressCreate(
                        time_id=new_time,
                        object_id=current_object.id,
                        progress=False
                    ),
                    db_session=db_session,
                )
                if rand_value < 0.37:
                    object_updated = await crud.object.update(
                        obj_current=current_object,
                        obj_new=IObjectUpdate(
                            status=ObjectStatus.READY
                        ),
                        db_session=db_session
                    )
                    if random() < 0.5:
                        new_time_1 = time_2023_id_first
                    else:
                        new_time_1 = time_2023_id
                    await crud.progress.create(
                        obj_in=IProgressCreate(
                            time_id=new_time_1,
                            object_id=object_updated.id,
                            progress=True
                        ),
                        db_session=db_session,
                    )
            logger.info(f"Project {p}")
