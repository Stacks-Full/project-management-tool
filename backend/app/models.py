from typing import Optional
from sqlmodel import SQLModel, Field


# The model must inherit from SQLModel, not Base
class Project(SQLModel, table=True):
    """
    Represents a project entity in the database.
    This is the core model for tracking project details.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)

def create_db_tables() -> None:
    """Attempts to create all defined tables in the connected database using SQLModel metadata."""
    # Import engine locally to avoid circular dependencies if models imports database
    from .database import engine
    print("Attempting to create database tables...")
    try:
        # We now use SQLModel.metadata, which finds all classes inheriting from SQLModel
        SQLModel.metadata.create_all(bind=engine)
        print("Database tables created successfully or already exist.")
    except Exception as e:
        print(f"Error creating tables: {e}")
