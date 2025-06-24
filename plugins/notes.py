"""
Notes plugin
Commands: save, note, notes, clear
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.helpers import edit_or_reply
from utils.database import Database

db = Database()

@Client.on_message(filters.command(["save"], Config.COMMAND_PREFIXES) & filters.me)
async def save_note(client: Client, message: Message):
    """Save a note"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.save [note_name] [content]`")
        return
    
    note_name = message.command[1].lower()
    
    if message.reply_to_message:
        content = message.reply_to_message.text or message.reply_to_message.caption or "Media"
    elif len(message.command) > 2:
        content = " ".join(message.command[2:])
    else:
        await edit_or_reply(message, "❌ **Please provide note content or reply to a message!**")
        return
    
    await db.add_note(message.chat.id, note_name, content)
    await edit_or_reply(message, f"📝 **Note saved:** `{note_name}`")

@Client.on_message(filters.command(["note"], Config.COMMAND_PREFIXES) & filters.me)
async def get_note(client: Client, message: Message):
    """Get a note"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.note [note_name]`")
        return
    
    note_name = message.command[1].lower()
    content = await db.get_note(message.chat.id, note_name)
    
    if not content:
        await edit_or_reply(message, f"❌ **Note not found:** `{note_name}`")
        return
    
    await edit_or_reply(message, f"📝 **Note:** `{note_name}`\n\n{content}")

@Client.on_message(filters.command(["notes"], Config.COMMAND_PREFIXES) & filters.me)
async def list_notes(client: Client, message: Message):
    """List all notes"""
    notes = await db.get_notes(message.chat.id)
    
    if not notes:
        await edit_or_reply(message, "❌ **No notes found in this chat!**")
        return
    
    note_list = "📝 **Notes in this chat:**\n\n"
    for note in notes:
        note_list += f"• `{note}`\n"
    
    await edit_or_reply(message, note_list)

@Client.on_message(filters.command(["clear"], Config.COMMAND_PREFIXES) & filters.me)
async def clear_note(client: Client, message: Message):
    """Clear/delete a note"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.clear [note_name]`")
        return
    
    note_name = message.command[1].lower()
    await db.delete_note(message.chat.id, note_name)
    await edit_or_reply(message, f"🗑️ **Note cleared:** `{note_name}`")

# Note handler for #notename
@Client.on_message(filters.regex(r"^#\w+") & ~filters.me & filters.group)
async def note_handler(client: Client, message: Message):
    """Handle note calls with #notename"""
    note_name = message.text[1:].lower()  # Remove # and convert to lowercase
    content = await db.get_note(message.chat.id, note_name)
    
    if content:
        await message.reply(f"📝 **{note_name}**\n\n{content}")