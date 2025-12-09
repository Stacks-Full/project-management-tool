from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    full_name: str
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Defines the full user data returned to the user themselves"""

    id: int
    full_name: str
    email: EmailStr
    username: str

    class Config:
        """Configuration to work with ORM objects."""

        from_attributes = True


class UserPublic(BaseModel):
    """Schema for user public"""

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

    access_token: str
    token_type: str = "bearer"
