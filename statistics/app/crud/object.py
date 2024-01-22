from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select

from app.crud.base import CRUDBase
from app.models.objects import Object, ObjectType
from app.schemas.object_schema import IObjectCreate, IObjectUpdate


class CRUDObject(CRUDBase[Object, IObjectCreate, IObjectUpdate]):
    async def get_by_real_object_id_and_object_type(
        self,
        *,
        real_object_id: UUID,
        object_type: ObjectType,
        db_session: AsyncSession | None = None
    ) -> Object | None:
        db_session = db_session or super().get_db().session
        query = select(Object).where(
            Object.real_object_id == real_object_id and
            Object.object_type == object_type
        )
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_object_id_by_real_object_id(
        self,
        *,
        real_object_id: UUID,
        object_type: ObjectType,
        db_session: AsyncSession | None = None
    ) -> UUID | None:
        db_session = db_session or super().get_db().session
        query = select(Object).where(
            Object.real_object_id == real_object_id and
            Object.object_type == object_type
        )
        response = await db_session.execute(query)
        current_object: Object = response.scalar_one_or_none()
        return current_object.id

    async def get_multi_by_subproject_id_paginated(
        self,
        *,
        subproject_id: UUID,
        params: Params | None,
        query: Object | Select[Object] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Page[Object]:
        if params is None:
            params = Params()
        db_session = db_session or self.db.session
        if query is None:
            query = select(Object).where(Object.subproject_id == subproject_id)
        return await paginate(db_session, query, params)


object = CRUDObject(Object)
