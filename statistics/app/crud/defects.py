from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import Defect
from app.schemas.defect_schema import IDefectCreate, IDefectUpdate


class CRUDDefect(CRUDBase[Defect, IDefectCreate, IDefectUpdate]):

    async def get_by_real_defect_id(
        self,
        *,
        real_defect_id: UUID,
        db_session: AsyncSession | None = None
    ) -> Defect | None:
        db_session = db_session or super().get_db().session
        query = select(Defect).where(Defect.defect_id == real_defect_id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()


defect = CRUDDefect(Defect)
