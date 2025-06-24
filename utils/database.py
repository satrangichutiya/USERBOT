import motor.motor_asyncio
import asyncio
from typing import Dict, Any, Optional
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)
            self.db = self.client[Config.DATABASE_NAME]
            # Test connection
            await self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB")
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("🔌 Disconnected from MongoDB")
    
    async def get_user_data(self, user_id: int) -> Dict[str, Any]:
        """Get user data"""
        if not self.db:
            return {}
        collection = self.db.users
        user_data = await collection.find_one({"user_id": user_id})
        return user_data or {}
    
    async def set_user_data(self, user_id: int, data: Dict[str, Any]):
        """Set user data"""
        if not self.db:
            return
        collection = self.db.users
        await collection.update_one(
            {"user_id": user_id},
            {"$set": data},
            upsert=True
        )
    
    async def get_chat_data(self, chat_id: int) -> Dict[str, Any]:
        """Get chat data"""
        if not self.db:
            return {}
        collection = self.db.chats
        chat_data = await collection.find_one({"chat_id": chat_id})
        return chat_data or {}
    
    async def set_chat_data(self, chat_id: int, data: Dict[str, Any]):
        """Set chat data"""
        if not self.db:
            return
        collection = self.db.chats
        await collection.update_one(
            {"chat_id": chat_id},
            {"$set": data},
            upsert=True
        )
    
    async def add_filter(self, chat_id: int, keyword: str, response: str):
        """Add a filter"""
        if not self.db:
            return
        collection = self.db.filters
        await collection.update_one(
            {"chat_id": chat_id, "keyword": keyword},
            {"$set": {"response": response}},
            upsert=True
        )
    
    async def get_filters(self, chat_id: int) -> list:
        """Get all filters for a chat"""
        if not self.db:
            return []
        collection = self.db.filters
        filters = await collection.find({"chat_id": chat_id}).to_list(None)
        return filters
    
    async def delete_filter(self, chat_id: int, keyword: str):
        """Delete a filter"""
        if not self.db:
            return
        collection = self.db.filters
        await collection.delete_one({"chat_id": chat_id, "keyword": keyword})
    
    async def add_note(self, chat_id: int, note_name: str, content: str):
        """Add a note"""
        if not self.db:
            return
        collection = self.db.notes
        await collection.update_one(
            {"chat_id": chat_id, "note_name": note_name},
            {"$set": {"content": content}},
            upsert=True
        )
    
    async def get_note(self, chat_id: int, note_name: str) -> Optional[str]:
        """Get a note"""
        if not self.db:
            return None
        collection = self.db.notes
        note = await collection.find_one({"chat_id": chat_id, "note_name": note_name})
        return note.get("content") if note else None
    
    async def get_notes(self, chat_id: int) -> list:
        """Get all notes for a chat"""
        if not self.db:
            return []
        collection = self.db.notes
        notes = await collection.find({"chat_id": chat_id}).to_list(None)
        return [note["note_name"] for note in notes]
    
    async def delete_note(self, chat_id: int, note_name: str):
        """Delete a note"""
        if not self.db:
            return
        collection = self.db.notes
        await collection.delete_one({"chat_id": chat_id, "note_name": note_name})