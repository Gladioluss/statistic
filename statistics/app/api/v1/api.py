from fastapi import APIRouter

from app.api.v1.endpoints import analytics

api_router_v1 = APIRouter()

api_router_v1.include_router(
    analytics.router,
    prefix="/v1/analytics",
    tags=["Analytics"])
