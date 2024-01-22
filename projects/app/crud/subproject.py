from sqlmodel import select, and_
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate

from app.crud.base import CRUDBase
from app.schemas.response_schema import Page
from app.schemas.subproject_schema import ISubprojectCreate, ISubprojectUpdate
from app.models.subproject import Subproject

class CRUDSubproject(CRUDBase[Subproject, ISubprojectCreate, ISubprojectUpdate]):
    async def get_paginated_list_by_status_id(
            self,
            status_id: UUID,
            params: Params = Params(),
            db_session: AsyncSession | None = None
    ) -> Page[Subproject]:
        db_session = db_session or super().get_db().session
        query = (
            select(Subproject).where(Subproject.status_id == status_id)
        )
        return await paginate(db_session, query, params)

    async def get_paginated_list_by_work_type_id(
            self,
            work_type_id: UUID,
            params: Params = Params(),
            db_session: AsyncSession | None = None
    ) -> Page[Subproject]:
        db_session = db_session or super().get_db().session
        query = (
            select(Subproject).where(Subproject.work_type_id == work_type_id)
        )
        return await paginate(db_session, query, params)

    async def get_paginated_list_by_project_id(
            self,
            project_id: UUID,
            params: Params = Params(),
            db_session: AsyncSession | None = None
    ) -> Page[Subproject]:
        db_session = db_session or super().get_db().session
        query = (
            select(Subproject).where(Subproject.project_id == project_id)
        )
        return await paginate(db_session, query, params)

    async def get_by_name_in_current_project(
            self,
            name: str,
            project_id: UUID,
            db_session: AsyncSession | None = None
    ) -> Subproject | None:
        db_session = db_session or self.db.session
        query = (
            select(Subproject).where(
                and_(
                    Subproject.name == name, Subproject.project_id == project_id
                )
            )
        )
        response = await db_session.execute(query)
        return response.scalar_one_or_none()


subproject = CRUDSubproject(Subproject)