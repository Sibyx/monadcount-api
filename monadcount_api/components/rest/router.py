from fastapi import APIRouter

from .endpoints import sync
from .endpoints import status

router = APIRouter()
router.include_router(sync.router, tags=["Synchronization"])
router.include_router(status.router, tags=["Status"])
