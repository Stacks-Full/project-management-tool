from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    """Schema for creating a new user."""

    full_name: str
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    is_online: bool

    class Config:
        """Configuration to work with ORM objects."""
        from_attributes = True

class TokenResponse(BaseModel):
    """Schema for token responce"""

    user_token: str
    