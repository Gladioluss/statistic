from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.orm import Load
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import Object
from app.models.projects import Project
from app.schemas.project_schema import IProjectCreate, IProjectUpdate


class CRUDProject(CRUDBase[Project, IProjectCreate, IProjectUpdate]):

    async def get_multi_paginated_without_subproject(
            self,
            *,
            params: Params | None,
            db_session: AsyncSession | None = None,
    ) -> Page[Project]:
        if params is None:
            params = Params()
        db_session = db_session or self.db.session
        res = select(Project).options(
            Load(
                Project
            ).noload("subprojects")
        )
        return await paginate(db_session, res, params)


    async def get_multi_paginated_without_progress(
            self,
            *,
            params: Params | None,
            db_session: AsyncSession | None = None,
    ) -> Page[Project]:
        if params is None:
            params = Params()
        db_session = db_session or self.db.session
        res = select(Project).options(
            Load(
                Object
            ).noload("progresses")
        )
        return await paginate(db_session, res, params)


    async def get_by_real_project_id(
        self,
        *,
        real_project_id: UUID,
        db_session: AsyncSession | None = None
    ) -> Project | None:
        db_session = db_session or super().get_db().session
        query = select(Project).where(Project.real_project_id == real_project_id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_project_id_by_real_project_id(
        self,
        *,
        real_project_id: UUID,
        db_session: AsyncSession | None = None
    ) -> UUID | None:
        db_session = db_session or super().get_db().session
        query = select(Project.id).where(Project.real_project_id == real_project_id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()


project = CRUDProject(Project)
