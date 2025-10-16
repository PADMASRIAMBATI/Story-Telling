from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import re
import logging
import bcrypt
import secrets

from app.core.config import settings

logger = logging.getLogger(__name__)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using bcrypt"""
    try:
        # Ensure both are bytes
        if isinstance(plain_password, str):
            plain_password = plain_password.encode('utf-8')
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Hash a password for storage using bcrypt"""
    try:
        # Convert to bytes and handle length limitation
        if isinstance(password, str):
            password_bytes = password.encode('utf-8')
        else:
            password_bytes = password
        
        # bcrypt has a 72-byte limit, so we need to handle this
        if len(password_bytes) > 72:
            logger.warning(f"Password truncated from {len(password_bytes)} to 72 bytes")
            password_bytes = password_bytes[:72]
        
        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=settings.SECURITY_BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string for storage
        return hashed.decode('utf-8')
        
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        raise ValueError("Failed to hash password")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"Token verification error: {e}")
        return None

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password meets minimum requirements"""
    if len(password) < settings.SECURITY_PASSWORD_MIN_LENGTH:
        return False
    # bcrypt limit is 72 bytes, but we'll be conservative with characters
    if len(password) > 70:  # Leave room for encoding
        return False
    return True