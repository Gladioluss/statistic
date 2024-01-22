from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy import exc
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import TowerDefects, TowerDefectsHistory
from app.schemas.tower_defects_history import ITowerDefectsHistoryCreate, ITowerDefectsHistoryUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDTowerDefectsHistory(
    CRUDBase[
        TowerDefectsHistory,
        ITowerDefectsHistoryCreate,
        ITowerDefectsHistoryUpdate
    ]
):
    async def create_from_tower_defects_obj(
            self,
            *,
            obj_in: TowerDefects,
            db_session: AsyncSession | None = None,
    ) -> TowerDefectsHistory:
        db_session = db_session or self.db.session
        db_obj = TowerDefectsHistory.from_orm(obj_in)  # type: ignore
        db_obj.main_id = obj_in.id
        try:
            db_session.add(db_obj)
            await db_session.commit()
        except exc.IntegrityError:
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            ) from exc
        await db_session.refresh(db_obj)
        return db_obj


tower_defects_history = CRUDTowerDefectsHistory(TowerDefectsHistory)
