from sqlmodel import select
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate

from app.schemas.response_schema import Page
from app.crud.base import CRUDBase
from app.schemas.project_schema import IProjectCreate, IProjectUpdate
from app.models.project import Project

class CRUDProject(CRUDBase[Project, IProjectCreate, IProjectUpdate]):
    async def get_paginated_list_by_status_id(
            self,
            status_id: UUID,
            params: Params = Params(),
            db_session: AsyncSession | None = None
    ) -> Page[Project]:
        db_session = db_session or super().get_db().session
        query = (
            select(Project).where(Project.status_id == status_id)
        )
        return await paginate(db_session, query, params)

    async def get_all(
            self,
            *,
            db_session: AsyncSession | None = None,
    ) -> list[Project]:
        db_session = db_session or self.db.session
        query = select(Project)
        response = await db_session.execute(query)
        return response.scalars().all()


project = CRUDProject(Project)