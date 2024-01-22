from sqlmodel import select, and_
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate

from app.schemas.response_schema import Page
from app.crud.base import CRUDBase
from app.schemas.span_schema import ISpanCreate, ISpanUpdate
from app.models.span import SpanEntity


class CRUDSpan(CRUDBase[SpanEntity, ISpanCreate, ISpanUpdate]):
    async def get_paginated_list_by_status_id(
            self,
            status_id: UUID,
            params: Params = Params(),
            db_session: AsyncSession | None = None
    ) -> Page[SpanEntity]:
        db_session = db_session or super().get_db().session
        query = (
            select(SpanEntity).where(SpanEntity.status_id == status_id)
        )
        return await paginate(db_session, query, params)

    async def get_paginated_list_by_object_id(
            self,
            object_id: UUID,
            params: Params = Params(),
            db_session: AsyncSession | None = None
    ) -> Page[SpanEntity]:
        db_session = db_session or super().get_db().session
        query = (
            select(SpanEntity).where(SpanEntity.object_id == object_id)
        )
        return await paginate(db_session, query, params)

    async def get_paginated_list_by_subproject_id(
            self,
            subproject_id: UUID,
            params: Params = Params(),
            db_session: AsyncSession | None = None
    ) -> Page[SpanEntity]:
        db_session = db_session or super().get_db().session
        query = (
            select(SpanEntity).where(SpanEntity.subproject_id == subproject_id)
        )
        return await paginate(db_session, query, params)

    async def get_by_name_in_current_subproject(
            self,
            name: str,
            subproject_id: UUID,
            db_session: AsyncSession | None = None
    ) -> SpanEntity | None:
        db_session = db_session or self.db.session
        query = (
            select(SpanEntity).where(
                and_(
                    SpanEntity.name == name, SpanEntity.subproject_id == subproject_id
                )
            )
        )
        response = await db_session.execute(query)
        return response.scalar_one_or_none()


span = CRUDSpan(SpanEntity)