from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import database
import os
from app.api import router as api_router
from app.services.exceptions import UserAlreadyExistsError
from app.core.exception_handlers import user_exists_exception_handler


database.wait_for_db()


def create_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application instance.
    Configures Cross-Origin Resource Sharing (CORS) middleware to allow all requests,
    and includes the main API router under the '/api' prefix.
    """
    app = FastAPI(
        title="Project Management API",
        description="FastAPI Backend for Project Management Tool",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(UserAlreadyExistsError, user_exists_exception_handler)
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()


@app.on_event("startup")
async def startup_event() -> None:
    """Handle application startup and initialize database connection."""
    print(" FastAPI Application Starting Up...")
    print(f" Connecting to DB at: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
