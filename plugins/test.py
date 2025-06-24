from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("test", prefixes=[".", "/", "!"]))
async def test_handler(_, message: Message):
    await message.reply_text("✅ Bot is working perfectly!")
