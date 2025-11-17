"""
Initialize all the routes in the application by importing them and including them in the /api endpoint
"""
from fastapi import APIRouter

from app.api.initial_routers import router as initial_router

router = APIRouter()
router.include_router(initial_router)
