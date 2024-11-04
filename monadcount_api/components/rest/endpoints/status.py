from fastapi import APIRouter
from monadcount_api.components.rest.schemas.status import StatusSchema

router = APIRouter()


@router.get("/status", response_model=StatusSchema)
async def created_token():
    return StatusSchema()
