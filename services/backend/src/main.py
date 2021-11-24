from fastapi import FastAPI

from src.api.api_v1.api import api_router

app = FastAPI(description='My API')

app.include_router(api_router, prefix='/api/v1')
