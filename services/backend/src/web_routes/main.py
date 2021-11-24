from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='src/templates')
router = APIRouter()



@router.get('/', include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse('index.html', {
        'request': request
    })
