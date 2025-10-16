import logging
from typing import Optional
from bson import ObjectId
from datetime import datetime

from app.core.database import db
from app.core.security import verify_password, get_password_hash, create_access_token, validate_email, validate_password
from app.models.user import User, UserCreate, UserLogin, UserResponse

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.users_collection = db.get_collection("users")
    
    def create_user(self, user_data: UserCreate) -> User:
        try:
            # Check if user already exists
            if self.users_collection.find_one({"email": user_data.email}):
                raise ValueError("User with this email already exists")
            
            if self.users_collection.find_one({"username": user_data.username}):
                raise ValueError("User with this username already exists")
            
            # Validate email
            if not validate_email(user_data.email):
                raise ValueError("Invalid email format")
            
            # Validate password
            if not validate_password(user_data.password):
                raise ValueError(f"Password must be at least {settings.SECURITY_PASSWORD_MIN_LENGTH} characters long and less than 70 characters")
            
            # Create user document
            user_dict = {
                "username": user_data.username,
                "email": user_data.email.lower(),
                "hashed_password": get_password_hash(user_data.password),
                "preferred_language": user_data.preferred_language,
                "role": "user",
                "story_count": 0,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert user
            result = self.users_collection.insert_one(user_dict)
            user_dict["id"] = str(result.inserted_id)
            
            logger.info(f"User created successfully: {user_data.email}")
            return User(**user_dict)
            
        except ValueError as ve:
            # Re-raise validation errors
            raise ve
        except Exception as e:
            logger.error(f"User creation failed: {str(e)}")
            raise ValueError(f"Failed to create user: {str(e)}")
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        try:
            user_data = self.users_collection.find_one({"email": email.lower()})
            if not user_data:
                logger.warning(f"Authentication failed: User not found for email {email}")
                return None
            
            # Convert ObjectId to string for the model
            user_data["id"] = str(user_data["_id"])
            del user_data["_id"]
            
            user = User(**user_data)
            
            if not verify_password(password, user.hashed_password):
                logger.warning(f"Authentication failed: Invalid password for email {email}")
                return None
            
            if not user.is_active:
                logger.warning(f"Authentication failed: User account inactive for email {email}")
                return None
            
            logger.info(f"Authentication successful for user: {email}")
            return user
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        try:
            if not ObjectId.is_valid(user_id):
                return None
            
            user_data = self.users_collection.find_one({"_id": ObjectId(user_id)})
            if not user_data:
                return None
            
            user_data["id"] = str(user_data["_id"])
            del user_data["_id"]
            return User(**user_data)
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            user_data = self.users_collection.find_one({"email": email.lower()})
            if not user_data:
                return None
            
            user_data["id"] = str(user_data["_id"])
            del user_data["_id"]
            return User(**user_data)
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            return None
    
    def create_access_token_for_user(self, user_id: str) -> str:
        return create_access_token({"sub": user_id})

# Global instance
auth_service = AuthService()