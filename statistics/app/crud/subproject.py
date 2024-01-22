from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.orm import Load
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.subprojects import Subproject
from app.schemas.subproject_schema import ISubprojectCreate, ISubprojectUpdate


class CRUDSubproject(CRUDBase[Subproject, ISubprojectCreate, ISubprojectUpdate]):

    async def get_by_real_subproject_id(
        self,
        *,
        real_subproject_id: UUID,
        db_session: AsyncSession | None = None
    ) -> Subproject | None:
        db_session = db_session or super().get_db().session
        query = select(Subproject).where(Subproject.real_subproject_id == real_subproject_id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_subproject_id_by_real_subproject_id(
        self,
        *,
        real_subproject_id: UUID,
        db_session: AsyncSession | None = None
    ) -> UUID | None:
        db_session = db_session or super().get_db().session
        query = select(Subproject.id).where(Subproject.real_subproject_id == real_subproject_id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_multi_paginated_without_object(
            self,
            *,
            params: Params | None,
            db_session: AsyncSession | None = None,
    ) -> Page[Subproject]:
        if params is None:
            params = Params()
        db_session = db_session or self.db.session
        res = select(Subproject).options(
            Load(
                Subproject
            ).noload("objects")
        )
        return await paginate(db_session, res, params)



subproject = CRUDSubproject(Subproject)
