"""
Fun commands plugin
Commands: toxic, god, nuke, otp, dna, virus, mood, namak, shayri, gali, hack
"""

import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.helpers import edit_or_reply, extract_user_info

# Fun responses and data
TOXIC_RESPONSES = [
    "🔥 Bro, you're so basic, even your WiFi password is '123456'!",
    "💀 You're like a software update - nobody wants you, but you keep showing up!",
    "😂 If stupidity was a superpower, you'd be Superman!",
    "🤡 You're proof that evolution can go in reverse!",
    "🎭 I'd explain it to you, but I don't have any crayons with me!",
    "💥 You're like a broken pencil - completely pointless!",
    "🌪️ If brains were dynamite, you wouldn't have enough to blow your nose!",
    "🎪 You're so dense, light bends around you!",
    "🔥 I've seen more intelligence in a brick wall!",
    "💀 You're like a participation trophy - everyone gets one, but nobody wants it!"
]

GOD_RESPONSES = [
    "⚡ I am the divine force that controls the digital realm!",
    "🌟 Mortal, you have summoned the almighty presence!",
    "👑 I am the supreme being of this chat, bow before my power!",
    "🔱 The gods have spoken through me, your wish is my command!",
    "⭐ I possess infinite wisdom and unlimited power!",
    "🌙 I am the moon god, illuminating the darkness of ignorance!",
    "🔥 My divine energy flows through every message!",
    "💫 I am omnipresent, omniscient, and omnipotent!",
    "🌈 I bring blessings and miracles to those who believe!",
    "⚡ Fear not, for I am here to guide you through the digital cosmos!"
]

VIRUS_MESSAGES = [
    "🦠 **VIRUS DETECTED!** Initiating system hack...",
    "💀 **MALWARE ACTIVATED!** Your device is now under my control!",
    "🔥 **TROJAN HORSE DEPLOYED!** Stealing all your data...",
    "⚡ **RANSOMWARE ATTACK!** Pay 1000 bitcoins to unlock!",
    "🌪️ **SYSTEM BREACH!** All your files are belong to us!",
    "💥 **NUCLEAR VIRUS!** Formatting hard drive in 3... 2... 1...",
    "🎭 **PHANTOM MALWARE!** I'm in your system, watching everything!",
    "🔱 **DIVINE VIRUS!** Even gods can't save you now!",
    "🌙 **MOON VIRUS!** Lunar power corrupting your device!",
    "💀 **DEATH VIRUS!** Your device's soul is now mine!"
]

DNA_RESULTS = [
    "🧬 **DNA Analysis Complete!**\n\n"
    "**Species:** Homo Sapiens (Barely)\n"
    "**Intelligence:** 12% (Below Average)\n"
    "**Humor Level:** 89% (Comedy Gold)\n"
    "**Weirdness:** 95% (Off the Charts)\n"
    "**Coolness Factor:** 67% (Pretty Cool)\n"
    "**Meme Potential:** 100% (Living Meme)",
    
    "🧬 **DNA Scan Results:**\n\n"
    "**Origin:** Planet Earth (Probably)\n"
    "**Brain Cells:** 3 (Still Functional)\n"
    "**Savage Level:** 78% (Roast Master)\n"
    "**Cringe Factor:** 45% (Tolerable)\n"
    "**Friendship Quality:** 92% (Keeper)\n"
    "**Overall Rating:** 8.5/10 (Would Recommend)"
]

MOOD_RESULTS = [
    "😊 **Happy** - Spreading positive vibes everywhere!",
    "😎 **Cool** - Too cool for school!",
    "🤔 **Thoughtful** - Deep in philosophical thoughts!",
    "😴 **Sleepy** - Needs more coffee!",
    "🔥 **Savage** - Roasting everyone in sight!",
    "🤪 **Crazy** - Absolutely bonkers!",
    "😇 **Angelic** - Pure and innocent soul!",
    "😈 **Devilish** - Up to some mischief!",
    "🥳 **Party Mode** - Ready to celebrate!",
    "🤓 **Nerdy** - Knowledge is power!"
]

SHAYRI_COLLECTION = [
    "🌙 चाँद की तरह चमकते रहो,\nसितारों की तरह टिमटिमाते रहो,\nजो भी हो जिंदगी में मुश्किल,\nहमेशा मुस्कुराते रहो! ✨",
    
    "💫 दिल में उम्मीद का दीया जलाए रखो,\nहर मुश्किल में खुद को संभाले रखो,\nवक्त बदलता रहता है यहाँ,\nअपने हौसले को बुलंद रखो! 🔥",
    
    "🌹 मोहब्बत में जो मिले वो कम है,\nजो न मिले वो भी कम नहीं,\nदिल की दुनिया बड़ी अजीब है,\nयहाँ कुछ भी कम नहीं! 💕"
]

GALI_COLLECTION = [
    "🤬 अबे साले, तेरा दिमाग घुटने में है क्या?",
    "😤 बेवकूफ, पहले अपना काम कर फिर दूसरों को सिखा!",
    "🙄 उल्लू के पट्ठे, समझ नहीं आता क्या?",
    "😠 गधे, थोड़ा दिमाग लगा के बात कर!",
    "🤦‍♂️ बुद्धू, इतना भी नहीं समझता?"
]

@Client.on_message(filters.command(["toxic"], Config.COMMAND_PREFIXES) & filters.me)
async def toxic_command(client: Client, message: Message):
    """Give toxic roast"""
    user_id, username = extract_user_info(message)
    
    if user_id or username:
        target = f"@{username}" if username else f"User {user_id}"
        response = f"{target} {random.choice(TOXIC_RESPONSES)}"
    else:
        response = random.choice(TOXIC_RESPONSES)
    
    await edit_or_reply(message, response)

@Client.on_message(filters.command(["god", "godmode"], Config.COMMAND_PREFIXES) & filters.me)
async def god_command(client: Client, message: Message):
    """God mode response"""
    response = random.choice(GOD_RESPONSES)
    await edit_or_reply(message, response)

@Client.on_message(filters.command(["nuke"], Config.COMMAND_PREFIXES) & filters.me)
async def nuke_command(client: Client, message: Message):
    """Simulate nuke attack"""
    msg = await edit_or_reply(message, "🚀 **LAUNCHING NUCLEAR STRIKE...**")
    await asyncio.sleep(1)
    await msg.edit("💥 **NUCLEAR WARHEAD ARMED!**")
    await asyncio.sleep(1)
    await msg.edit("🌪️ **IMPACT IN 3...**")
    await asyncio.sleep(1)
    await msg.edit("💀 **2...**")
    await asyncio.sleep(1)
    await msg.edit("☢️ **1...**")
    await asyncio.sleep(1)
    await msg.edit("🔥💥💀 **BOOM! CHAT NUKED!** 💀💥🔥\n\n*Just kidding! Everyone's safe! 😄*")

@Client.on_message(filters.command(["otp"], Config.COMMAND_PREFIXES) & filters.me)
async def otp_command(client: Client, message: Message):
    """Generate random OTP"""
    otp = random.randint(1000, 999999)
    await edit_or_reply(message, f"🔐 **Your OTP:** `{otp}`\n\n*Valid for 5 minutes*")

@Client.on_message(filters.command(["dna"], Config.COMMAND_PREFIXES) & filters.me)
async def dna_command(client: Client, message: Message):
    """DNA analysis"""
    user_id, username = extract_user_info(message)
    
    if user_id or username:
        target = f"@{username}" if username else f"User {user_id}"
        result = random.choice(DNA_RESULTS)
        response = f"🧬 **DNA Analysis for {target}:**\n\n{result}"
    else:
        response = "🧬 **Please reply to a user or mention someone for DNA analysis!**"
    
    await edit_or_reply(message, response)

@Client.on_message(filters.command(["virus"], Config.COMMAND_PREFIXES) & filters.me)
async def virus_command(client: Client, message: Message):
    """Simulate virus attack"""
    user_id, username = extract_user_info(message)
    
    if user_id or username:
        target = f"@{username}" if username else f"User {user_id}"
        virus_msg = random.choice(VIRUS_MESSAGES)
        response = f"{virus_msg}\n\n**Target:** {target}\n\n*Just a prank! No actual harm done! 😄*"
    else:
        response = f"{random.choice(VIRUS_MESSAGES)}\n\n*Just a prank! 😄*"
    
    await edit_or_reply(message, response)

@Client.on_message(filters.command(["mood"], Config.COMMAND_PREFIXES) & filters.me)
async def mood_command(client: Client, message: Message):
    """Check user mood"""
    user_id, username = extract_user_info(message)
    
    if user_id or username:
        target = f"@{username}" if username else f"User {user_id}"
        mood = random.choice(MOOD_RESULTS)
        response = f"🎭 **Mood Analysis for {target}:**\n\n{mood}"
    else:
        response = "🎭 **Please reply to a user or mention someone for mood analysis!**"
    
    await edit_or_reply(message, response)

@Client.on_message(filters.command(["namak", "roast"], Config.COMMAND_PREFIXES) & filters.me)
async def namak_command(client: Client, message: Message):
    """Roast with spicy logic"""
    user_id, username = extract_user_info(message)
    
    roasts = [
        "🧂 You're like salt - a little goes a long way, but you're everywhere!",
        "🌶️ Spicier than your personality, that's for sure!",
        "🔥 You're so salty, the Dead Sea is jealous!",
        "💀 Even my roasts need seasoning after meeting you!",
        "🎭 You're like expired salt - useless and bitter!"
    ]
    
    if user_id or username:
        target = f"@{username}" if username else f"User {user_id}"
        response = f"{target} {random.choice(roasts)}"
    else:
        response = random.choice(roasts)
    
    await edit_or_reply(message, response)

@Client.on_message(filters.command(["shayri", "poetry"], Config.COMMAND_PREFIXES) & filters.me)
async def shayri_command(client: Client, message: Message):
    """Send beautiful shayri"""
    shayri = random.choice(SHAYRI_COLLECTION)
    await edit_or_reply(message, shayri)

@Client.on_message(filters.command(["gali", "abuse"], Config.COMMAND_PREFIXES) & filters.me)
async def gali_command(client: Client, message: Message):
    """Send gali (for fun)"""
    user_id, username = extract_user_info(message)
    
    if user_id or username:
        target = f"@{username}" if username else f"User {user_id}"
        gali = random.choice(GALI_COLLECTION)
        response = f"{target} {gali}"
    else:
        response = random.choice(GALI_COLLECTION)
    
    await edit_or_reply(message, response)

@Client.on_message(filters.command(["hack"], Config.COMMAND_PREFIXES) & filters.me)
async def hack_command(client: Client, message: Message):
    """Simulate hacking"""
    user_id, username = extract_user_info(message)
    
    if user_id or username:
        target = f"@{username}" if username else f"User {user_id}"
        msg = await edit_or_reply(message, f"🔓 **Initiating hack on {target}...**")
        await asyncio.sleep(1)
        await msg.edit(f"💻 **Connecting to {target}'s device...**")
        await asyncio.sleep(1)
        await msg.edit(f"🔍 **Scanning for vulnerabilities...**")
        await asyncio.sleep(1)
        await msg.edit(f"⚡ **Exploiting security flaws...**")
        await asyncio.sleep(1)
        await msg.edit(f"📱 **Accessing {target}'s data...**")
        await asyncio.sleep(1)
        await msg.edit(f"✅ **HACK SUCCESSFUL!**\n\n"
                      f"**Target:** {target}\n"
                      f"**Status:** Pwned 😎\n"
                      f"**Data Stolen:** Everything! 💀\n\n"
                      f"*Just kidding! This is just for fun! 😄*")
    else:
        await edit_or_reply(message, "🔓 **Please reply to a user or mention someone to 'hack'!**")

# Auto features
auto_shayri_enabled = {}
auto_gali_enabled = {}
auto_hack_enabled = {}

@Client.on_message(filters.command(["autoshayri"], Config.COMMAND_PREFIXES) & filters.me)
async def auto_shayri_toggle(client: Client, message: Message):
    """Toggle auto shayri"""
    chat_id = message.chat.id
    
    if chat_id in auto_shayri_enabled:
        del auto_shayri_enabled[chat_id]
        await edit_or_reply(message, "📴 **Auto Shayri Disabled!**")
    else:
        auto_shayri_enabled[chat_id] = True
        await edit_or_reply(message, "📱 **Auto Shayri Enabled!**\n\nI'll send random shayri in this chat!")

@Client.on_message(filters.command(["autogali"], Config.COMMAND_PREFIXES) & filters.me)
async def auto_gali_toggle(client: Client, message: Message):
    """Toggle auto gali"""
    chat_id = message.chat.id
    
    if chat_id in auto_gali_enabled:
        del auto_gali_enabled[chat_id]
        await edit_or_reply(message, "📴 **Auto Gali Disabled!**")
    else:
        auto_gali_enabled[chat_id] = True
        await edit_or_reply(message, "📱 **Auto Gali Enabled!**\n\nI'll roast people randomly in this chat!")

@Client.on_message(filters.command(["autohack"], Config.COMMAND_PREFIXES) & filters.me)
async def auto_hack_toggle(client: Client, message: Message):
    """Toggle auto hack"""
    chat_id = message.chat.id
    
    if chat_id in auto_hack_enabled:
        del auto_hack_enabled[chat_id]
        await edit_or_reply(message, "📴 **Auto Hack Disabled!**")
    else:
        auto_hack_enabled[chat_id] = True
        await edit_or_reply(message, "📱 **Auto Hack Enabled!**\n\nI'll 'hack' people randomly in this chat!")

# Auto message handlers
@Client.on_message(filters.text & ~filters.me)
async def auto_features_handler(client: Client, message: Message):
    """Handle auto features"""
    chat_id = message.chat.id
    
    # Auto Shayri (5% chance)
    if chat_id in auto_shayri_enabled and random.randint(1, 100) <= 5:
        shayri = random.choice(SHAYRI_COLLECTION)
        await message.reply(shayri)
    
    # Auto Gali (3% chance)
    elif chat_id in auto_gali_enabled and random.randint(1, 100) <= 3:
        gali = random.choice(GALI_COLLECTION)
        await message.reply(f"@{message.from_user.username or message.from_user.first_name} {gali}")
    
    # Auto Hack (2% chance)
    elif chat_id in auto_hack_enabled and random.randint(1, 100) <= 2:
        target = f"@{message.from_user.username or message.from_user.first_name}"
        hack_msg = f"🔓 **Auto-hacking {target}...** 💻\n\n*Prank mode activated!* 😄"
        await message.reply(hack_msg)