from uuid import UUID

from aio_pika.abc import AbstractIncomingMessage

from app import crud
from app.core.config import settings
from app.database.session import SessionLocal
from app.schemas.progress_schema import IProgressCreate
from app.schemas.time_schema import ITimeCreate
from app.utils.checks.time_checks import check_time_exists


async def new_progress(object_id: UUID, message: AbstractIncomingMessage):
    """
    Create a progress from rabbit queued messages

    :param object_id: UUID
    :param message: AbstractIncomingMessage
    :return: None
    """
    async with SessionLocal() as session:
        time = ITimeCreate()
        current_time = await check_time_exists(
            time=time,
            db_session=session
        )
        if current_time is None:
            new_time = await crud.time.create(obj_in=time, db_session=session)
        else:
            new_time = current_time
        status = True if message.headers["Status"] == settings.OBJECT_AVAILABILITY_STATUS else False

        await crud.progress.create(
            obj_in=IProgressCreate(
                time_id=new_time.id,
                object_id=object_id,
                progress=status
            ),
            db_session=session,
        )

