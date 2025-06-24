#!/usr/bin/env python3
"""
🌙 Moon UserBot - Advanced Telegram UserBot
Version: 3.4.5
Author: Moon Team
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

from pyrogram import Client
from config import Config
from utils.database import Database
from utils.helpers import load_plugins, setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

class MoonUserBot:
    def __init__(self):
        self.app = Client(
            "moon_userbot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            session_string=Config.SESSION_STRING,
            plugins=dict(root="plugins")
        )
        self.db = Database()

    async def start(self):
        """Start the userbot"""
        try:
            await self.app.start()
            me = await self.app.get_me()
            logger.info(f"🌙 Moon UserBot Started Successfully!")
            logger.info(f"👤 User: {me.first_name} (@{me.username})")
            logger.info(f"📱 Phone: {me.phone_number}")
            logger.info(f"🆔 User ID: {me.id}")
            logger.info(f"🔧 Total Plugins: {len(os.listdir('plugins'))}")

            # Initialize database
            await self.db.connect()

            # Send alive message if log chat is configured
            if Config.LOG_CHAT:
                try:
                    await self.app.send_message(
                        Config.LOG_CHAT,
                        f"🌙 **Moon UserBot Started!**\n\n"
                        f"👤 **User:** {me.first_name}\n"
                        f"🆔 **ID:** `{me.id}`\n"
                        f"📱 **Phone:** `{me.phone_number}`\n"
                        f"🔧 **Plugins:** `{len(os.listdir('plugins'))}`\n"
                        f"🚀 **Version:** `3.4.5`"
                    )
                except Exception as e:
                    logger.error(f"Failed to send alive message: {e}")

        except Exception as e:
            logger.error(f"❌ Failed to start userbot: {e}")
            sys.exit(1)

    async def stop(self):
        """Stop the userbot"""
        await self.app.stop()
        await self.db.disconnect()
        logger.info("🌙 Moon UserBot Stopped!")

# Global userbot instance
moon = MoonUserBot()

async def main():
    """Main function"""
    try:
        await moon.start()
        await asyncio.Event().wait()  # Keeps bot running (replacement for .idle())
    except KeyboardInterrupt:
        logger.info("🛑 Received interrupt signal")
    finally:
        await moon.stop()

if __name__ == "__main__":
    asyncio.run(main())
