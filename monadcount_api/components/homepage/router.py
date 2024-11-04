from fastapi import APIRouter

from .endpoints import homepage

router = APIRouter()
router.include_router(homepage.router)
