from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from sqlalchemy.orm import Session

from monadcount_api.core import templates
from monadcount_api.db import get_db

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request=request, name="index.html", context={"hello": "world"})
