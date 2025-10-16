from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn

from app.core.config import settings
from app.core.database import db
from app.services.nlp_service import nlp_service
from app.api import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In the lifespan function, update the NLP service initialization:
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    
    # 1. Database Connection
    try:
        # Connect to database
        if not db.connect():
            # Don't raise, but log a critical error. The app can still run if the DB is optional, 
            # but here it's mandatory, so we rely on the log and health check.
            logger.error("❌ Failed to connect to database. DB is disconnected.")
            
    except Exception as e:
        logger.error(f"❌ Database connection failed during startup: {e}")
        pass
        
    # 2. NLP Service Initialization (Model Loading)
    try:
        # Initialize NLP service (this will load all models, including LoRA if present)
        await nlp_service.initialize()
        logger.info("✅ StoryGenie AI models loaded successfully.")
        
    except Exception as e:
        logger.error(f"❌ AI Model Loading failed: {e}")
        logger.info("❌ StoryGenie starting without AI generation capabilities. Check Hugging Face key or memory.")

    yield
    
    # Shutdown
    db.close()
    await nlp_service.close()
    logger.info("✅ StoryGenie shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if db.client and nlp_service.is_initialized else "degraded",
        "database": "connected" if db.client else "disconnected",
        "nlp_service": "ready" if nlp_service.is_initialized else "failed_to_load"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )