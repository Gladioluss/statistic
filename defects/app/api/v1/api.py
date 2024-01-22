from fastapi import APIRouter

from app.api.v1.endpoints import (
    string_defect_types,
    string_defects,
    string_defects_history,
    tower_defect_types,
    tower_defects,
    tower_defects_history,
    track_defect_types,
    track_defects,
    wire_defect_types,
    wire_defects,
    wire_defects_history,
)

api_router_v1 = APIRouter()

api_router_v1.include_router(
    string_defect_types.router,
    prefix="/v1/string_defect_types",
    tags=["string_defect_types"])

api_router_v1.include_router(
    string_defects.router,
    prefix="/v1/string_defects",
    tags=["string_defects"]
)

api_router_v1.include_router(
    string_defects_history.router,
    prefix="/v1/string_defects_history",
    tags=["string_defects_history"]
)

api_router_v1.include_router(
    tower_defect_types.router,
    prefix="/v1/tower_defect_types",
    tags=["tower_defect_types"]
)

api_router_v1.include_router(
    tower_defects.router,
    prefix="/v1/tower_defects",
    tags=["tower_defects"]
)

api_router_v1.include_router(
    tower_defects_history.router,
    prefix="/v1/tower_defects_history",
    tags=["tower_defects_history"]
)

api_router_v1.include_router(
    track_defect_types.router,
    prefix="/v1/track_defect_types",
    tags=["track_defect_types"]
)

api_router_v1.include_router(
    track_defects.router,
    prefix="/v1/track_defects",
    tags=["track_defects"]
)

api_router_v1.include_router(
    wire_defect_types.router,
    prefix="/v1/wire_defect_types",
    tags=["wire_defect_types"]
)

api_router_v1.include_router(
    wire_defects.router,
    prefix="/v1/wire_defects",
    tags=["wire_defects"]
)

api_router_v1.include_router(
    wire_defects_history.router,
    prefix="/v1/wire_defects_history",
    tags=["wire_defects_history"]
)
