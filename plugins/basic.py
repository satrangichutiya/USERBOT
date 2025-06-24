"""
Basic commands plugin
Commands: ping, help, alive, restart
"""

import time
import psutil
import platform
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.helpers import edit_or_reply, get_readable_time, get_size

@Client.on_message(filters.command(["ping", "p"], Config.COMMAND_PREFIXES) & filters.me)
async def ping_command(client: Client, message: Message):
    """Check bot ping"""
    start = time.time()
    msg = await edit_or_reply(message, "🏓 **Pinging...**")
    end = time.time()
    ping_time = (end - start) * 1000
    
    uptime = get_readable_time(int(time.time() - psutil.boot_time()))
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    text = (
        f"🏓 **Pong!**\n\n"
        f"📡 **Ping:** `{ping_time:.2f} ms`\n"
        f"⏰ **Uptime:** `{uptime}`\n"
        f"🖥️ **CPU:** `{cpu_usage}%`\n"
        f"💾 **RAM:** `{memory.percent}%`\n"
        f"💿 **Disk:** `{disk.percent}%`\n"
        f"🐍 **Python:** `{platform.python_version()}`\n"
        f"🌙 **Moon UserBot:** `v3.4.5`"
    )
    
    await msg.edit(text)

@Client.on_message(filters.command(["alive", "awake"], Config.COMMAND_PREFIXES) & filters.me)
async def alive_command(client: Client, message: Message):
    """Check if bot is alive"""
    me = await client.get_me()
    uptime = get_readable_time(int(time.time() - psutil.boot_time()))
    
    text = (
        f"🌙 **Moon UserBot is Alive!**\n\n"
        f"👤 **User:** {me.first_name}\n"
        f"🆔 **ID:** `{me.id}`\n"
        f"📱 **Phone:** `{me.phone_number}`\n"
        f"⏰ **Uptime:** `{uptime}`\n"
        f"🚀 **Version:** `3.4.5`\n"
        f"🐍 **Python:** `{platform.python_version()}`\n\n"
        f"{Config.ALIVE_TEXT}"
    )
    
    if Config.ALIVE_PIC:
        await message.reply_photo(Config.ALIVE_PIC, caption=text)
        await message.delete()
    else:
        await edit_or_reply(message, text)

@Client.on_message(filters.command(["help", "h"], Config.COMMAND_PREFIXES) & filters.me)
async def help_command(client: Client, message: Message):
    """Show help menu"""
    if len(message.command) > 1:
        # Show help for specific module
        module = message.command[1].lower()
        # This would be implemented based on plugin documentation
        await edit_or_reply(message, f"📚 Help for module: **{module}**\n\nModule help would be shown here.")
    else:
        # Show main help menu
        text = (
            f"🌙 **Moon UserBot Help Menu**\n"
            f"**Version:** `3.4.5`\n"
            f"**Total Modules:** `300+`\n\n"
            f"**📋 Categories:**\n"
            f"• 🔧 **Basic** - Essential commands\n"
            f"• 🎭 **Fun** - Entertainment commands\n"
            f"• 🛡️ **Admin** - Administration tools\n"
            f"• 🌐 **Web** - Web-related tools\n"
            f"• 📱 **Social** - Social media tools\n"
            f"• 🎵 **Music** - Music commands\n"
            f"• 📊 **Stats** - Statistics and info\n"
            f"• 🔒 **Security** - Security features\n"
            f"• 🎨 **Media** - Media manipulation\n"
            f"• 🤖 **AI** - AI-powered features\n\n"
            f"**Usage:** `.help [module]` for specific help\n"
            f"**Prefix:** `{Config.DEFAULT_PREFIX}`"
        )
        await edit_or_reply(message, text)

@Client.on_message(filters.command(["restart", "reboot"], Config.COMMAND_PREFIXES) & filters.me)
async def restart_command(client: Client, message: Message):
    """Restart the userbot"""
    await edit_or_reply(message, "🔄 **Restarting Moon UserBot...**")
    import os
    import sys
    os.execl(sys.executable, sys.executable, *sys.argv)