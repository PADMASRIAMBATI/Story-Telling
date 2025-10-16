from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
import logging

from app.models.user import UserCreate, UserLogin
from app.services.auth_service import auth_service
from app.core.security import validate_email

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=Dict[str, Any])
async def register(user_data: UserCreate):
    """
    Register a new user
    """
    try:
        logger.info(f"Registration attempt for email: {user_data.email}")
        
        # Create user
        user = auth_service.create_user(user_data)
        
        # Create access token
        access_token = auth_service.create_access_token_for_user(str(user.id))
        
        return {
            "message": "User registered successfully",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "preferred_language": user.preferred_language,
                "story_count": user.story_count
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except ValueError as e:
        logger.warning(f"Registration validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )

@router.post("/login", response_model=Dict[str, Any])
async def login(login_data: UserLogin):
    """
    Login user and return access token
    """
    try:
        logger.info(f"Login attempt for email: {login_data.email}")
        
        # Authenticate user
        user = auth_service.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token = auth_service.create_access_token_for_user(str(user.id))
        
        return {
            "message": "Login successful",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "preferred_language": user.preferred_language,
                "story_count": user.story_count
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )