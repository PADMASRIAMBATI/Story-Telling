from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StoryList(BaseModel):
    id: str
    title: str
    genre: str
    language: str
    length: str
    word_count: int
    created_at: datetime

class StoryHistory(BaseModel):
    stories: List[StoryList]
    total_count: int