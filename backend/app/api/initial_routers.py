from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core import database, models

router = APIRouter()

@router.get("/")
def root() -> dict[str, str]:
    """Return a simple status message indicating the API is running."""
    return {"message": "Project Management API is running!"}

@router.get("/health", tags=["Health Check"])
def health_check(db: Session = Depends(database.get_session)) -> dict[str, str]:
    """Check the API status and database connection."""
    try:
        # Try to execute a simple query to ensure the DB connection is live
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@router.get("/status", tags=["Health Check"])
def status_check(db: Session = Depends(database.get_session)) -> dict[str, str]:
    """Check the API status and database connection."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

