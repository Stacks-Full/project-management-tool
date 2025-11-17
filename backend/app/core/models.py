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

class Users(SQLModel, table=True):
    """
    Represents a user entity in the database.
    This is the core model for tracking user details
    """
    user_id: Optional[int] = Field(default=None, primary_key=True)
    fullname: str = Field(index=True, max_length=255)
    username: Optional[str] = Field(default=None, max_length=255)
    hashed_password: str = Field(index=True, max_length=255)
