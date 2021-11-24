from fastapi import APIRouter

from src.api.api_v1.endpoints import customers

api_router = APIRouter()

api_router.include_router(customers.router, prefix='/customers', tags=['customers'])
