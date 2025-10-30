from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models
import os
import time
from sqlalchemy import text
import MySQLdb

# Create the tables on startup
def wait_for_db():
    """Wait for database to be ready"""
    max_retries = 10
    for i in range(max_retries):
        try:
            models.create_db_tables()
            print("✅ Database tables created successfully!")
            return
        except Exception as e:
            print(f"⏳ Database not ready yet (attempt {i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                time.sleep(5)
            else:
                print("❌ Could not connect to database after multiple attempts")
                raise

wait_for_db()

app = FastAPI(
    title="Project Management API",
    description="FastAPI Backend for Project Management Tool",
    version="0.1.0",
)

# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI Application Starting Up...")
    print(f"📊 Connecting to DB at: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")

@app.get("/")
def root():
    return {"message": "Project Management API is running!"}

@app.get("/health", tags=["Health Check"])
def health_check(db: Session = Depends(get_db)):
    """Check the API status and database connection."""
    try:
        # Try to execute a simple query to ensure the DB connection is live
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.get("/status", tags=["Health Check"])
def status_check(db: Session = Depends(get_db)):
    """Check the API status and database connection."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Your existing project endpoints...
