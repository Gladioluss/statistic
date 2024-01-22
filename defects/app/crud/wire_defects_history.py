from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy import exc
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import WireDefects
from app.models.wire_defects_history import WireDefectsHistory
from app.schemas.wire_defects_history import IWireDefectsHistoryCreate, IWireDefectsHistoryUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDWireDefectsHistory(
    CRUDBase[
        WireDefectsHistory,
        IWireDefectsHistoryCreate,
        IWireDefectsHistoryUpdate
    ]
):
    async def create_from_wire_defects_obj(
            self,
            *,
            obj_in: WireDefects,
            db_session: AsyncSession | None = None,
    ) -> WireDefectsHistory:
        db_session = db_session or self.db.session
        db_obj = WireDefectsHistory.from_orm(obj_in)  # type: ignore
        db_obj.main_id = obj_in.id
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


wire_defects_history = CRUDWireDefectsHistory(WireDefectsHistory)
