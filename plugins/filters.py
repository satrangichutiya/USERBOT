"""
Filters plugin
Commands: filter, filters, fdel, fsearch
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.helpers import edit_or_reply
from utils.database import Database

db = Database()

@Client.on_message(filters.command(["filter"], Config.COMMAND_PREFIXES) & filters.me)
async def add_filter(client: Client, message: Message):
    """Add a filter"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.filter [keyword] [response]`")
        return
    
    if not message.reply_to_message and len(message.command) < 3:
        await edit_or_reply(message, "❌ **Please provide both keyword and response!**")
        return
    
    keyword = message.command[1].lower()
    
    if message.reply_to_message:
        response = message.reply_to_message.text or message.reply_to_message.caption or "Media"
    else:
        response = " ".join(message.command[2:])
    
    await db.add_filter(message.chat.id, keyword, response)
    await edit_or_reply(message, f"✅ **Filter added for:** `{keyword}`")

@Client.on_message(filters.command(["filters"], Config.COMMAND_PREFIXES) & filters.me)
async def list_filters(client: Client, message: Message):
    """List all filters"""
    chat_filters = await db.get_filters(message.chat.id)
    
    if not chat_filters:
        await edit_or_reply(message, "❌ **No filters found in this chat!**")
        return
    
    filter_list = "📝 **Filters in this chat:**\n\n"
    for filter_data in chat_filters:
        filter_list += f"• `{filter_data['keyword']}`\n"
    
    await edit_or_reply(message, filter_list)

@Client.on_message(filters.command(["fdel", "delfilter"], Config.COMMAND_PREFIXES) & filters.me)
async def delete_filter(client: Client, message: Message):
    """Delete a filter"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.fdel [keyword]`")
        return
    
    keyword = message.command[1].lower()
    await db.delete_filter(message.chat.id, keyword)
    await edit_or_reply(message, f"🗑️ **Filter deleted:** `{keyword}`")

@Client.on_message(filters.command(["fsearch"], Config.COMMAND_PREFIXES) & filters.me)
async def search_filter(client: Client, message: Message):
    """Search for a filter"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.fsearch [keyword]`")
        return
    
    keyword = message.command[1].lower()
    chat_filters = await db.get_filters(message.chat.id)
    
    found_filters = [f for f in chat_filters if keyword in f['keyword']]
    
    if not found_filters:
        await edit_or_reply(message, f"❌ **No filters found containing:** `{keyword}`")
        return
    
    result = f"🔍 **Filters containing '{keyword}':**\n\n"
    for filter_data in found_filters:
        result += f"• `{filter_data['keyword']}`\n"
    
    await edit_or_reply(message, result)

# Filter handler
@Client.on_message(filters.text & ~filters.me & filters.group)
async def filter_handler(client: Client, message: Message):
    """Handle filter responses"""
    if not message.text:
        return
    
    chat_filters = await db.get_filters(message.chat.id)
    if not chat_filters:
        return
    
    text = message.text.lower()
    
    for filter_data in chat_filters:
        if filter_data['keyword'] in text:
            await message.reply(filter_data['response'])
            break