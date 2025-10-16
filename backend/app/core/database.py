from pymongo import MongoClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
    
    def connect(self):
        try:
            self.client = MongoClient(settings.MONGODB_URI)
            self.db = self.client[settings.DATABASE_NAME]
            # Test connection
            self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB")
            return True
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            return False
    
    def get_collection(self, collection_name: str):
        if self.db is None:
            if not self.connect():
                raise Exception("Database connection failed")
        return self.db[collection_name]
    
    def close(self):
        if self.client:
            self.client.close()
            logger.info("✅ MongoDB connection closed")

# Global database instance
db = Database()

def get_database():
    return db