from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core import database
import os
import time
from sqlalchemy import text
from app.api import router as api_router

database.wait_for_db()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Project Management API",
        description="FastAPI Backend for Project Management Tool",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.include_router(api_router, prefix='/api')
    return app

app = create_app()

@app.on_event("startup")
async def startup_event() -> None:
    """Handle application startup and initialize database connection."""
    print(" FastAPI Application Starting Up...")
    print(f" Connecting to DB at: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
