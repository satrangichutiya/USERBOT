import logging
import os
import sys
import importlib
import asyncio
import time
import random
import string
from typing import List, Dict, Any
from pathlib import Path
from pyrogram.types import Message
from config import Config

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('moon_userbot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def load_plugins():
    """Load all plugins from plugins directory"""
    plugins_dir = Path("plugins")
    if not plugins_dir.exists():
        return []
    
    plugins = []
    for file in plugins_dir.glob("*.py"):
        if file.name.startswith("_"):
            continue
        module_name = f"plugins.{file.stem}"
        try:
            importlib.import_module(module_name)
            plugins.append(file.stem)
        except Exception as e:
            logging.error(f"Failed to load plugin {file.stem}: {e}")
    
    return plugins

def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format"""
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    
    time_list.reverse()
    ping_time += ":".join(time_list)
    
    return ping_time

def get_size(bytes: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} PB"

async def edit_or_reply(message: Message, text: str, **kwargs):
    """Edit message if it's from self, otherwise reply"""
    if message.from_user and message.from_user.is_self:
        return await message.edit(text, **kwargs)
    else:
        return await message.reply(text, **kwargs)

def generate_random_string(length: int = 10) -> str:
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def extract_user_info(message: Message):
    """Extract user info from message"""
    user_id = None
    username = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
    elif len(message.command) > 1:
        if message.command[1].isdigit():
            user_id = int(message.command[1])
        elif message.command[1].startswith("@"):
            username = message.command[1][1:]
    
    return user_id, username

def format_exc(e: Exception) -> str:
    """Format exception for logging"""
    return f"{type(e).__name__}: {str(e)}"

async def run_sync(func, *args, **kwargs):
    """Run sync function in executor"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)

def get_command_prefix(message: Message) -> str:
    """Get command prefix from message"""
    text = message.text or message.caption or ""
    for prefix in Config.COMMAND_PREFIXES:
        if text.startswith(prefix):
            return prefix
    return Config.DEFAULT_PREFIX

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == Config.OWNER_ID or user_id in Config.SUDO_USERS

class Progress:
    """Progress tracker for uploads/downloads"""
    def __init__(self, message: Message, action: str):
        self.message = message
        self.action = action
        self.start_time = time.time()
        self.last_update = 0
    
    async def update(self, current: int, total: int):
        """Update progress"""
        now = time.time()
        if now - self.last_update < 2:  # Update every 2 seconds
            return
        
        self.last_update = now
        percentage = current * 100 / total
        speed = current / (now - self.start_time)
        eta = (total - current) / speed if speed > 0 else 0
        
        progress_bar = "█" * int(percentage / 10) + "░" * (10 - int(percentage / 10))
        
        text = (
            f"**{self.action}**\n\n"
            f"`{progress_bar}` {percentage:.1f}%\n\n"
            f"**Size:** {get_size(current)} / {get_size(total)}\n"
            f"**Speed:** {get_size(speed)}/s\n"
            f"**ETA:** {get_readable_time(int(eta))}"
        )
        
        try:
            await self.message.edit(text)
        except:
            pass