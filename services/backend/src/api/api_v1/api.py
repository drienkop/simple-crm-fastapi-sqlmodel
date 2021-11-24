from fastapi import APIRouter

from src.api.api_v1.endpoints import customers, products

api_router = APIRouter()

api_router.include_router(customers.router, prefix='/customers', tags=['customers'])
api_router.include_router(products.router, prefix='/products', tags=['products'])
