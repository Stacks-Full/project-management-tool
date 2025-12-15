from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.services.user_service import UserService
from app.api.schemas.user_schemas import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": dict,
            "description": "Username or Email already exists."
        }
    }
)
def register_user(
    user_data: UserCreate,

    # Dependency Injection for DB Session
    db: Session = Depends(get_session) ):

    # Instantiate the Service Layer
    user_service = UserService()

    # Call all the service (validation, hashing, and saving happens here)
    new_user = user_service.create_user(db=db, user_data=user_data)

    # On success, the return value is automatically converted to UserResponse
    return new_user
