from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Time
from app.schemas.time_schema import ITimeCreate


async def check_time_exists(
    time: ITimeCreate,
    db_session: AsyncSession
) -> Time | None:
    response = await db_session.execute(
        select(Time).filter(
            and_(
                Time.day_of_month == time.day_of_month,
                Time.month == time.month,
                Time.year == time.year
            )
        )
    )
    return response.scalar_one_or_none()
