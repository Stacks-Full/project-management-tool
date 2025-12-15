from sqlalchemy.orm import Session
from app.core import models
from app.core.models import User

from app.api.schemas.user_schemas import UserCreate
from .exceptions import UserAlreadyExistsError
from .security import hash_password
from sqlalchemy import or_

class UserService:
    # Set up the signature which receive a session and the data model
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        # Check for existing user
        existing_user = db.query(User).filter(
            or_(
                User.email == user_data.email,
                User.username == user_data.username
            )
        ).first()

        # Handle the duplicate case
        if existing_user: 
            # First check which field cause the error
            if existing_user.email == user_data.email:
                raise UserAlreadyExistsError("Email is already registered.")
            elif existing_user.username == user_data.username:
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

