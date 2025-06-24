import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Pyrogram Configuration
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    SESSION_STRING = os.getenv("SESSION_STRING", "")
    
    # Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
    SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "").split()))
    
    # Database Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "moon_userbot")
    REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")
    
    # Prefixes and Commands
    COMMAND_PREFIXES = [".", "!", "?", "/", "~", "+", "*"]
    DEFAULT_PREFIX = "."
    
    # Features Configuration
    PMPERMIT = bool(os.getenv("PMPERMIT", "True"))
    ANTI_SPAM = bool(os.getenv("ANTI_SPAM", "True"))
    AUTO_READ = bool(os.getenv("AUTO_READ", "False"))
    
    # External APIs
    WEATHER_API = os.getenv("WEATHER_API", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_CHAT = int(os.getenv("LOG_CHAT", "0"))
    
    # Heroku Configuration
    HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "")
    HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "")
    
    # GitHub Configuration
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    
    # Telegraph Configuration
    TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN", "")
    
    # Misc
    TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
    ALIVE_PIC = os.getenv("ALIVE_PIC", "")
    ALIVE_TEXT = os.getenv("ALIVE_TEXT", "🌙 Moon UserBot is Alive!")