from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated

from app import crud
from app.models.span import SpanEntity
from app.utils.exceptions.common import (
    NameNotFoundException,
    IdNotFoundException,
)


async def get_span_by_id_from_path(
        id: Annotated[UUID, Path(description="The UUID id of the span")]
) -> SpanEntity:
    span = await crud.span.get(id=id)
    if not span:
        raise IdNotFoundException(SpanEntity, id=id)
    return span


async def get_span_by_id_from_query(
        id: Annotated[UUID, Query(description="The UUID id of the span")]
) -> SpanEntity:
    span = await crud.span.get(id=id)
    if not span:
        raise IdNotFoundException(SpanEntity, id=id)
    return span