import logging
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.core.database import db
from app.models.story import Story, StoryCreate, StoryResponse
from app.models.user import User

logger = logging.getLogger(__name__)

class StoryService:
    def __init__(self):
        self.stories_collection = db.get_collection("stories")
        self.users_collection = db.get_collection("users")
    
    async def create_story(self, story_data: StoryCreate, user_id: str) -> Story:
        try:
            # Generate title from prompt
            title = self._generate_title(story_data.prompt)
            
            # Create story document
            story_dict = {
                "user_id": ObjectId(user_id),
                "title": title,
                "prompt": story_data.prompt,
                "genre": story_data.genre.value,
                "language": story_data.language.value,
                "length": story_data.length.value,
                "tone": story_data.tone.value if story_data.tone else None,
                "characters": story_data.characters,
                "setting": story_data.setting,
                "content": "",  # Will be filled by NLP service
                "word_count": 0,
                "is_favorite": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert story
            result = self.stories_collection.insert_one(story_dict)
            
            # Get the inserted story with proper ID
            inserted_story = self.stories_collection.find_one({"_id": result.inserted_id})
            
            if not inserted_story:
                raise ValueError("Failed to retrieve created story")
            
            # Convert to Story model
            inserted_story["id"] = str(inserted_story["_id"])
            inserted_story["user_id"] = str(inserted_story["user_id"])
            del inserted_story["_id"]
            
            # Update user's story count
            self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"story_count": 1}}
            )
            
            logger.info(f"Story created successfully with ID: {inserted_story['id']}")
            return Story(**inserted_story)
            
        except Exception as e:
            logger.error(f"Story creation failed: {str(e)}")
            raise ValueError(f"Failed to create story: {str(e)}")
    
    async def get_story_by_id(self, story_id: str, user_id: str) -> Optional[Story]:
        try:
            if not ObjectId.is_valid(story_id):
                return None
            
            story_data = self.stories_collection.find_one({
                "_id": ObjectId(story_id),
                "user_id": ObjectId(user_id)
            })
            
            if not story_data:
                return None
            
            story_data["id"] = str(story_data["_id"])
            story_data["user_id"] = str(story_data["user_id"])
            del story_data["_id"]
            
            return Story(**story_data)
        except Exception as e:
            logger.error(f"Error getting story: {str(e)}")
            return None
    
    async def get_user_stories(self, user_id: str, skip: int = 0, limit: int = 20) -> List[Story]:
        try:
            stories_data = self.stories_collection.find({
                "user_id": ObjectId(user_id)
            }).sort("created_at", -1).skip(skip).limit(limit)
            
            stories = []
            for story_data in stories_data:
                story_data["id"] = str(story_data["_id"])
                story_data["user_id"] = str(story_data["user_id"])
                del story_data["_id"]
                stories.append(Story(**story_data))
            
            return stories
        except Exception as e:
            logger.error(f"Error getting user stories: {str(e)}")
            return []
    
    async def update_story_content(self, story_id: str, user_id: str, content: str, word_count: int) -> bool:
        try:
            if not ObjectId.is_valid(story_id):
                logger.error(f"Invalid story ID: {story_id}")
                return False
            
            result = self.stories_collection.update_one(
                {"_id": ObjectId(story_id), "user_id": ObjectId(user_id)},
                {
                    "$set": {
                        "content": content,
                        "word_count": word_count,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            success = result.modified_count > 0
            if success:
                logger.info(f"Story content updated successfully for story: {story_id}")
            else:
                logger.warning(f"No story found to update: {story_id}")
            
            return success
        except Exception as e:
            logger.error(f"Error updating story content: {str(e)}")
            return False
    
    def _generate_title(self, prompt: str) -> str:
        """Generate a title from the prompt"""
        words = prompt.split()[:6]
        title = ' '.join(words)
        if len(prompt.split()) > 6:
            title += '...'
        return title

# Global instance
story_service = StoryService()