from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
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
        from_attributes = True

class tokenresponse(BaseModel):
    user_token: str
    
