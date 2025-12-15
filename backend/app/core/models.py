from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Represents a user entity in the database.
    This is the core model for tracking user details
    """
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(index=True, max_length=255)
    email: str = Field(index=True, unique=True, max_length=255)
    username: str = Field(index=True, unique=True, max_length=50)
    hashed_password: str = Field(index=False, max_length=255)
    user_token: Optional[str] = Field(default=None, max_length=1024)
