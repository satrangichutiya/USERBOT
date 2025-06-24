#!/usr/bin/env python3
"""
🌙 Moon UserBot - FIXED MAIN.PY
"""

import asyncio
import logging
import os
import sys

from pyrogram import Client
from config import Config
from utils.database import Database
from utils.helpers import setup_logging

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
        try:
            await self.app.start()
            me = await self.app.get_me()
            logger.info("🌙 Moon UserBot Started Successfully!")
            logger.info(f"👤 User: {me.first_name} (@{me.username})")
            logger.info(f"📱 Phone: {me.phone_number}")
            logger.info(f"🆔 User ID: {me.id}")
            logger.info(f"🔧 Total Plugins: {len(os.listdir('plugins'))}")

            await self.db.connect()

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
                    logger.warning(f"⚠️ Failed to send log message: {e}")
        except Exception as e:
            logger.error(f"❌ Failed to start: {e}")
            sys.exit(1)

    async def run_forever(self):
        logger.info("🔁 Running UserBot... (Press CTRL+C to stop)")
        while True:
            await asyncio.sleep(10)

    async def stop(self):
        await self.app.stop()
        await self.db.disconnect()
        logger.info("🛑 Moon UserBot Stopped!")


moon = MoonUserBot()

async def main():
    try:
        await moon.start()
        await moon.run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("🔌 Gracefully stopping...")
    finally:
        await moon.stop()

if __name__ == "__main__":
    asyncio.run(main())
