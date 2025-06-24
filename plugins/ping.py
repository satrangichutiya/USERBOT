import time
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("ping", prefixes=[".", "/", "!"]))
async def ping_handler(client, message: Message):
    start = time.time()

    sent = await message.reply_text("🏓 Pinging...")

    end = time.time()
    ping_time = (end - start) * 1000
    ping_str = f"{ping_time:.2f} ms"

    await sent.edit_text(
        f"""
<b>🔧 PONG!</b>
🌀 <b>Latency:</b> <code>{ping_str}</code>
🤖 <b>UserBot:</b> Moon 3.4.5
🚀 <b>Status:</b> <i>Online & Working</i>
"""
    )
