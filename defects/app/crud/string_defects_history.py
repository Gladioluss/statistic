from typing import TypeVar

from sqlalchemy import exc
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.exceptions import HTTPException

from app.crud.base import CRUDBase
from app.models import StringDefects, StringDefectsHistory
from app.schemas.string_defects_history import IStringDefectsHistoryCreate, IStringDefectsHistoryUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class CRUDStringDefectsHistory(
    CRUDBase[
        StringDefectsHistory,
        IStringDefectsHistoryCreate,
        IStringDefectsHistoryUpdate
    ]
):
    async def create_from_string_defects_obj(
            self,
            *,
            obj_in: StringDefects,
            db_session: AsyncSession | None = None,
    ) -> StringDefectsHistory:
        db_session = db_session or self.db.session
        db_obj = StringDefectsHistory.from_orm(obj_in)  # type: ignore
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


string_defects_history = CRUDStringDefectsHistory(StringDefectsHistory)
