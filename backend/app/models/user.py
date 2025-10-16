from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi" 
    TELUGU = "te"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=255)
    preferred_language: Language = Language.ENGLISH

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)  # Max 72 for bcrypt
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if len(v) > 72:
            raise ValueError('Password must be less than 72 characters long')
        return v
    
    @validator('email')
    def email_valid(cls, v):
        from app.core.security import validate_email
        if not validate_email(v):
            raise ValueError('Invalid email format')
        return v.lower()

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: Optional[str] = None
    hashed_password: str
    role: str = "user"
    story_count: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    preferred_language: str
    story_count: int