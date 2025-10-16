from pydantic import BaseModel
from datetime import datetime

class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    preferred_language: str
    story_count: int
    total_words: int
    created_at: datetime

class UserStats(BaseModel):
    total_stories: int
    total_words: int
    favorite_stories: int
    genres_explored: list
    languages_used: list