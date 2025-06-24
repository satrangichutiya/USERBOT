"""
PM Permit plugin - Private message permission system
Commands: approve, disapprove, block, unblock
"""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.helpers import edit_or_reply
from utils.database import Database

db = Database()

# PM Permit settings
PMPERMIT_TEXT = """
🌙 **Moon UserBot PM Security**

Hello! This is an automated message.

🔒 **You are not approved to PM me.**
📝 **Please state your reason for messaging.**
⚠️ **Spamming will result in a block.**

**Commands for owner:**
• `.approve` - Approve user
• `.block` - Block user
• `.disapprove` - Remove approval

*Powered by Moon UserBot v3.4.5*
"""

@Client.on_message(filters.command(["approve"], Config.COMMAND_PREFIXES) & filters.me)
async def approve_user(client: Client, message: Message):
    """Approve a user for PM"""
    if message.chat.type != "private":
        if not message.reply_to_message:
            await edit_or_reply(message, "❌ **Reply to a user to approve them!**")
            return
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.chat.id
    
    # Add user to approved list
    user_data = await db.get_user_data(user_id)
    user_data['approved'] = True
    await db.set_user_data(user_id, user_data)
    
    try:
        user = await client.get_users(user_id)
        name = user.first_name
    except:
        name = f"User {user_id}"
    
    await edit_or_reply(message, f"✅ **Approved {name} for PM!**")

@Client.on_message(filters.command(["disapprove"], Config.COMMAND_PREFIXES) & filters.me)
async def disapprove_user(client: Client, message: Message):
    """Remove approval from a user"""
    if message.chat.type != "private":
        if not message.reply_to_message:
            await edit_or_reply(message, "❌ **Reply to a user to disapprove them!**")
            return
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.chat.id
    
    # Remove user from approved list
    user_data = await db.get_user_data(user_id)
    user_data['approved'] = False
    await db.set_user_data(user_id, user_data)
    
    try:
        user = await client.get_users(user_id)
        name = user.first_name
    except:
        name = f"User {user_id}"
    
    await edit_or_reply(message, f"❌ **Disapproved {name} from PM!**")

@Client.on_message(filters.command(["block"], Config.COMMAND_PREFIXES) & filters.me)
async def block_user(client: Client, message: Message):
    """Block a user"""
    if message.chat.type != "private":
        if not message.reply_to_message:
            await edit_or_reply(message, "❌ **Reply to a user to block them!**")
            return
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.chat.id
    
    try:
        await client.block_user(user_id)
        
        # Add to blocked list in database
        user_data = await db.get_user_data(user_id)
        user_data['blocked'] = True
        user_data['approved'] = False
        await db.set_user_data(user_id, user_data)
        
        try:
            user = await client.get_users(user_id)
            name = user.first_name
        except:
            name = f"User {user_id}"
        
        await edit_or_reply(message, f"🚫 **Blocked {name}!**")
    
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["unblock"], Config.COMMAND_PREFIXES) & filters.me)
async def unblock_user(client: Client, message: Message):
    """Unblock a user"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.unblock [user_id/username]`")
        return
    
    try:
        if message.command[1].isdigit():
            user_id = int(message.command[1])
        else:
            user = await client.get_users(message.command[1])
            user_id = user.id
        
        await client.unblock_user(user_id)
        
        # Remove from blocked list in database
        user_data = await db.get_user_data(user_id)
        user_data['blocked'] = False
        await db.set_user_data(user_id, user_data)
        
        try:
            user = await client.get_users(user_id)
            name = user.first_name
        except:
            name = f"User {user_id}"
        
        await edit_or_reply(message, f"✅ **Unblocked {name}!**")
    
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["pmpermit"], Config.COMMAND_PREFIXES) & filters.me)
async def toggle_pmpermit(client: Client, message: Message):
    """Toggle PM permit on/off"""
    user_data = await db.get_user_data(message.from_user.id)
    current_status = user_data.get('pmpermit', True)
    
    new_status = not current_status
    user_data['pmpermit'] = new_status
    await db.set_user_data(message.from_user.id, user_data)
    
    status_text = "✅ **Enabled**" if new_status else "❌ **Disabled**"
    await edit_or_reply(message, f"🔒 **PM Permit {status_text}!**")

# PM Permit handler
@Client.on_message(filters.private & ~filters.me & ~filters.bot)
async def pmpermit_handler(client: Client, message: Message):
    """Handle PM permit"""
    # Check if PM permit is enabled
    owner_data = await db.get_user_data(Config.OWNER_ID)
    if not owner_data.get('pmpermit', Config.PMPERMIT):
        return
    
    user_id = message.from_user.id
    
    # Skip if user is owner or sudo user
    if user_id == Config.OWNER_ID or user_id in Config.SUDO_USERS:
        return
    
    # Check if user is approved
    user_data = await db.get_user_data(user_id)
    if user_data.get('approved', False):
        return
    
    # Check if user is blocked
    if user_data.get('blocked', False):
        return
    
    # Check if we already sent PM permit message
    if user_data.get('pmpermit_sent', False):
        # Increment spam count
        spam_count = user_data.get('spam_count', 0) + 1
        user_data['spam_count'] = spam_count
        await db.set_user_data(user_id, user_data)
        
        # Auto-block after 5 messages
        if spam_count >= 5:
            try:
                await client.block_user(user_id)
                user_data['blocked'] = True
                await db.set_user_data(user_id, user_data)
                
                # Notify owner
                if Config.LOG_CHAT:
                    await client.send_message(
                        Config.LOG_CHAT,
                        f"🚫 **Auto-blocked user for spamming PM**\n\n"
                        f"**User:** {message.from_user.first_name}\n"
                        f"**ID:** `{user_id}`\n"
                        f"**Username:** @{message.from_user.username or 'None'}\n"
                        f"**Spam Count:** `{spam_count}`"
                    )
            except:
                pass
        return
    
    # Send PM permit message
    try:
        await message.reply(PMPERMIT_TEXT)
        user_data['pmpermit_sent'] = True
        user_data['spam_count'] = 1
        await db.set_user_data(user_id, user_data)
        
        # Notify owner about new PM
        if Config.LOG_CHAT:
            await client.send_message(
                Config.LOG_CHAT,
                f"📨 **New PM from unapproved user**\n\n"
                f"**User:** {message.from_user.first_name}\n"
                f"**ID:** `{user_id}`\n"
                f"**Username:** @{message.from_user.username or 'None'}\n"
                f"**Message:** {message.text[:100]}..."
            )
    
    except Exception as e:
        pass

@Client.on_message(filters.command(["pmguard"], Config.COMMAND_PREFIXES) & filters.me)
async def pm_guard_status(client: Client, message: Message):
    """Show PM guard status and statistics"""
    # Get statistics
    # This would require more complex database queries in a real implementation
    
    owner_data = await db.get_user_data(Config.OWNER_ID)
    pmpermit_status = owner_data.get('pmpermit', Config.PMPERMIT)
    
    status_text = (
        f"🔒 **PM Guard Status**\n\n"
        f"**Status:** {'✅ Enabled' if pmpermit_status else '❌ Disabled'}\n"
        f"**Auto-block after:** `5 messages`\n"
        f"**Approved Users:** `Loading...`\n"
        f"**Blocked Users:** `Loading...`\n\n"
        f"**Commands:**\n"
        f"• `.approve` - Approve user\n"
        f"• `.disapprove` - Remove approval\n"
        f"• `.block` - Block user\n"
        f"• `.unblock` - Unblock user\n"
        f"• `.pmpermit` - Toggle PM permit"
    )
    
    await edit_or_reply(message, status_text)