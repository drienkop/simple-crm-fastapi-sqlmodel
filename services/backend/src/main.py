from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.api_v1.api import api_router
from src.web_routes import main

app = FastAPI(title='Simple-CRM',
              version='1.0.0',
              description='Simple-CRM API is your gateway to the CRM backend.')

app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(api_router, prefix='/api/v1')
app.include_router(main.router)
