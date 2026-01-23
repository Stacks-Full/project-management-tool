from sqlalchemy.orm import Session
from app.core.models import User

from app.api.schemas.user_schemas import UserCreate, TokenResponse, UserLogin
from .exceptions import UserAlreadyExistsError, UnAuthorizedLoginError, BadRequestError
from .security import hash_password, token_secret_retrival, token_string_randomizer, token_algorithim_retrival, verify_password
from sqlalchemy import or_
import jwt
from datetime import timedelta, datetime, timezone

class UserService:
    """Service class for handling all User-related business logic and database interactions"""

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        """Creates a new User after checking for duplicate email or username"""
        # Check for existing user
        existing_user = (
            db.query(User)
            .filter(or_(User.email == user_data.email, User.username == user_data.username))
            .first()
        )

        # Handle the duplicate case
        if existing_user:
            # First check which field cause the error
            if existing_user.email == user_data.email:
                raise UserAlreadyExistsError("Email is already registered.")

            if existing_user.username == user_data.username:
                raise UserAlreadyExistsError("Username is already taken.")

        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Create a new User object
        user_data_dict = user_data.model_dump(exclude={"password"})
        new_user = User(**user_data_dict, hashed_password=hashed_password)

        # Database logic for persist and return
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    def user_login_create_token(self, db: Session, user_data:UserLogin) -> TokenResponse:
        
        user = db.query(User).filter(User.email == user_data.email).first()

        if not user:
            raise UnAuthorizedLoginError("Invalid email or password")
        
        if not verify_password(user_data.password, user.hashed_password):
            raise UnAuthorizedLoginError("Invalid email or password")
        
        payload = {
            "user_id": user.user_id,
            "jti": token_string_randomizer(),
            "exp": datetime.now(timezone.utc) + timedelta(seconds=3600),
        }

        secret = token_secret_retrival()

        algoithim = token_algorithim_retrival()

        access_token = jwt.encode(payload, secret, algoithim)

        user.user_token = access_token
        db.add(user)
        db.commit()
        db.refresh(user)

        return TokenResponse(access_token=access_token)