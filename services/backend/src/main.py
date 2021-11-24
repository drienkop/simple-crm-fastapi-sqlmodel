from fastapi import FastAPI

from src.api.api_v1.api import api_router

app = FastAPI(title='Simple-CRM',
              version='1.0.0',
              description='Simple-CRM API is your gateway to the CRM backend.')

app.include_router(api_router, prefix='/api/v1')
