from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    username: str
    hashed_password: str

class UserResponse(BaseModel):
    full_name: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str 


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    user_token: str
    is_online = bool
    is_ofline = bool

    class Config:
        from_attributes = True
    
