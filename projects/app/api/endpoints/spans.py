from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params
from typing import Annotated

from app import crud
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    IDeleteResponseBase,
    create_response,
)
from app.schemas.span_schema import *
from app.utils.exceptions.common import IdNotFoundException, NameExistException
from app.models.span import SpanEntity
from app.models.status import ObjectStatus
from app.models.subproject import Subproject
from app.deps import object_status_deps, subproject_deps, span_deps
from app.utils.checks import object_status_checks, subproject_checks, span_checks

router = APIRouter()


@router.get("/list")
async def get_spans(
        params: Params = Depends()
) -> IGetResponsePaginated[ISpanRead]:
    """
    Gets a paginated list of spans
    """
    spans = await crud.span.get_multi_paginated(params=params)
    return create_response(data=spans)


@router.get("/list/status")
async def get_spans_list_by_status_id(
        current_object_status: ObjectStatus = Depends(object_status_deps.get_object_status_by_id_from_query),
        params: Params = Depends()
) -> IGetResponsePaginated[ISpanRead]:
    """
    Gets a paginated list of spans by status id
    """
    spans = await crud.span.get_paginated_list_by_status_id(
        status_id=current_object_status.id,
        params=params
    )
    return create_response(data=spans)


@router.get("/list/subproject")
async def get_spans_list_by_subproject_id(
        current_subproject: Subproject = Depends(subproject_deps.get_subproject_by_id_from_query),
        params: Params = Depends()
) -> IGetResponsePaginated[ISpanRead]:
    """
    Gets a paginated list of spans by subproject id
    """
    spans = await crud.span.get_paginated_list_by_subproject_id(
        subproject_id=current_subproject.id,
        params=params
    )
    return create_response(data=spans)


@router.get("/{id}")
async def read_span_by_id(
        span: SpanEntity = Depends(span_deps.get_span_by_id_from_path)
) -> IGetResponseBase[ISpanRead]:
    """
    Gets a span by id
    """
    return create_response(data=span)


@router.get("/{id}/status")
async def get_span_with_object_status_by_id(
        span: SpanEntity = Depends(span_deps.get_span_by_id_from_path)
) -> IGetResponseBase[ISpanWithObjectStatusRead]:
    """
    Gets a span with status by id
    """
    return create_response(data=span)


@router.get("/{id}/subproject")
async def get_span_with_subproject_by_id(
        span: SpanEntity = Depends(span_deps.get_span_by_id_from_path)
) -> IGetResponseBase[ISpanWithSubprojectRead]:
    """
    Gets a span with subproject by id
    """
    return create_response(data=span)


@router.get("/{id}/full")
async def get_span_with_subproject_and_status_by_id(
        span: SpanEntity = Depends(span_deps.get_span_by_id_from_path)
) -> IGetResponseBase[ISpanWithFullInfoRead]:
    """
    Gets a span with subproject and status by id
    """
    return create_response(data=span)


@router.post("")
async def create_span(
        span: ISpanCreate
) -> IPostResponseBase[ISpanRead]:
    """
    Creates a new span
    """
    await subproject_checks.subproject_is_exist(id=span.subproject_id)
    await span_checks.span_name_is_taken_in_current_subproject(name=span.name, subproject_id=span.subproject_id)
    if span.status_id:
        await object_status_checks.object_status_is_exist(id=span.status_id)

    new_span = await crud.subproject.create(obj_in=span)
    return create_response(data=new_span)


@router.put("/{id}")
async def update_span(
        span: ISpanUpdate,
        current_span: SpanEntity = Depends(span_deps.get_span_by_id_from_path)
) -> IPutResponseBase[ISpanRead]:
    """
    Updates a span by its id
    """
    if span.subproject_id:
        await subproject_checks.subproject_is_exist(id=span.subproject_id)
        if span.name:
            await span_checks.span_name_is_taken_in_current_subproject(name=span.name, subproject_id=span.subproject_id)
        if not span.name:
            await span_checks.span_name_is_taken_in_current_subproject(name=current_span.name,
                                                                       subproject_id=span.subproject_id)
    if not span.subproject_id:
        if span.name:
            await span_checks.span_name_is_taken_in_current_subproject(name=span.name,
                                                                       subproject_id=current_span.subproject_id)

    if span.status_id:
        await object_status_checks.object_status_is_exist(id=span.status_id)
    if span.subproject_id:
        await subproject_checks.subproject_is_exist(id=span.subproject_id)

    span_updated = await crud.span.update(obj_current=current_span, obj_new=span)
    return create_response(data=span_updated)


@router.delete("/{id}")
async def delete_span(
        current_span: SpanEntity = Depends(span_deps.get_span_by_id_from_path)
) -> IDeleteResponseBase[ISpanRead]:
    """
    Deletes a span by its id
    """
    span_deleted = await crud.span.remove(id=current_span.id)
    return create_response(data=span_deleted)