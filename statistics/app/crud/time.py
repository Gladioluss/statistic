from fastapi import HTTPException
from sqlalchemy import exc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.times import Time
from app.schemas.time_schema import ITimeCreate, ITimeUpdate


class CRUDTime(CRUDBase[Time, ITimeCreate, ITimeUpdate]):
    async def setup_time(
            self,
            *,
            obj_in: ITimeCreate | Time,
            db_session: AsyncSession | None = None,
    ) -> Time:
        db_session = db_session or self.db.session
        db_obj = self.model.from_orm(obj_in)  # type: ignore

        try:
            db_session.add(db_obj)
            await db_session.commit()
        except exc.IntegrityError:
            await db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            ) from exc
        await db_session.refresh(db_obj)
        return db_obj


time = CRUDTime(Time)
