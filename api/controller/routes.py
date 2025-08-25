from fastapi import APIRouter
from api.controller.v1.endpoints.recommender import router

api_router = APIRouter()

api_router.include_router(router, prefix="/recommend", tags=["recommend"])
