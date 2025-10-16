from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Genre(str, Enum):
    FANTASY = "fantasy"
    MYSTERY = "mystery"
    HORROR = "horror"
    ROMANCE = "romance"
    SCIFI = "sci-fi"
    ADVENTURE = "adventure"
    HISTORICAL = "historical"
    COMEDY = "comedy"

class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    TELUGU = "te"

class Length(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"

class Tone(str, Enum):
    DRAMATIC = "dramatic"
    LIGHT_HEARTED = "light_hearted"
    HUMOROUS = "humorous"
    DARK = "dark"
    SERIOUS = "serious"

class Story(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: str
    prompt: str
    genre: str  # Changed from Genre to str for flexibility
    language: str  # Changed from Language to str
    length: str  # Changed from Length to str
    tone: Optional[str] = None  # Changed from Tone to str
    characters: Optional[List[str]] = None
    setting: Optional[str] = None
    content: str
    word_count: int
    is_favorite: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StoryCreate(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    genre: Genre
    language: Language
    length: Length
    tone: Optional[Tone] = None
    characters: Optional[List[str]] = None
    setting: Optional[str] = None

class StoryResponse(BaseModel):
    id: str
    title: str
    prompt: str
    genre: str
    language: str
    length: str
    tone: Optional[str]
    characters: Optional[List[str]]
    setting: Optional[str]
    content: str
    word_count: int
    is_favorite: bool
    created_at: datetime