from fastapi import APIRouter, HTTPException, status, Depends, Query, Header
from typing import List, Dict, Any, Optional
import logging

from app.models.story import StoryCreate, StoryResponse
from app.models.user import User
from app.services.story_service import story_service
from app.services.nlp_service import nlp_service
from app.services.auth_service import auth_service
from app.core.security import verify_token
# Remove PDF service import and Response import

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_current_user(authorization: str = Header(...)) -> User:
    """Dependency to get current user from JWT token"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = authorization[7:]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@router.post("/generate", response_model=Dict[str, Any])
async def generate_story(
    story_data: StoryCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a new story using AI
    """
    try:
        logger.info(f"Generating story for user: {current_user.username}")
        
        # Create story in database
        story = await story_service.create_story(story_data, str(current_user.id))
        logger.info(f"Story created with ID: {story.id}")
        
        # Prepare data for AI generation
        generation_data = {
            "prompt": story_data.prompt,
            "genre": story_data.genre.value,
            "language": story_data.language.value,
            "length": story_data.length.value,
            "tone": story_data.tone.value if story_data.tone else "light_hearted",
            "characters": story_data.characters,
            "setting": story_data.setting
        }
        
        # Generate story content using AI
        generated_content = await nlp_service.generate_story(generation_data)
        logger.info(f"Story content generated, length: {len(generated_content)}")
        
        # Update story with generated content
        word_count = len(generated_content.split())
        success = await story_service.update_story_content(
            str(story.id), 
            str(current_user.id), 
            generated_content, 
            word_count
        )
        
        if not success:
            logger.error(f"Failed to update story content for story: {story.id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save generated story"
            )
        
        # Get updated story
        updated_story = await story_service.get_story_by_id(str(story.id), str(current_user.id))
        
        if not updated_story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Story not found after generation"
            )
        
        return {
            "message": "Story generated successfully",
            "story": {
                "id": str(updated_story.id),
                "title": updated_story.title,
                "prompt": updated_story.prompt,
                "genre": updated_story.genre,
                "language": updated_story.language,
                "length": updated_story.length,
                "tone": updated_story.tone,
                "characters": updated_story.characters,
                "setting": updated_story.setting,
                "content": updated_story.content,
                "word_count": updated_story.word_count,
                "is_favorite": updated_story.is_favorite,
                "created_at": updated_story.created_at
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Story generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during story generation"
        )

@router.get("/", response_model=Dict[str, Any])
async def get_user_stories(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get all stories for the current user
    """
    try:
        stories = await story_service.get_user_stories(str(current_user.id), skip, limit)
        
        return {
            "stories": [
                {
                    "id": str(story.id),
                    "title": story.title,
                    "genre": story.genre,
                    "language": story.language,
                    "length": story.length,
                    "word_count": story.word_count,
                    "created_at": story.created_at
                }
                for story in stories
            ],
            "total_count": len(stories),
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting user stories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{story_id}", response_model=Dict[str, Any])
async def get_story(
    story_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific story by ID
    """
    try:
        story = await story_service.get_story_by_id(story_id, str(current_user.id))
        if not story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Story not found"
            )
        
        return {
            "message": "Story retrieved successfully",
            "story": {
                "id": str(story.id),
                "title": story.title,
                "prompt": story.prompt,
                "genre": story.genre,
                "language": story.language,
                "length": story.length,
                "tone": story.tone,
                "characters": story.characters,
                "setting": story.setting,
                "content": story.content,
                "word_count": story.word_count,
                "is_favorite": story.is_favorite,
                "created_at": story.created_at
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting story: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
