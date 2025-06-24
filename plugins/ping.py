from pyrogram import Client, filters
from pyrogram.types import Message
import time

@Client.on_message(filters.command("ping", prefixes=[".", "/", "!"]) & filters.me)
async def ping(_, message: Message):
    start = time.time()
    sent = await message.reply("🔁 Testing Ping...")
    end = time.time()

    latency = (end - start) * 1000
    await sent.edit(
        f"""
<b>🏓 PING REPORT</b>
🧠 <b>User:</b> {message.from_user.mention}
📶 <b>Latency:</b> <code>{latency:.2f} ms</code>
🚀 <b>Status:</b> Active & OP
"""
    )
