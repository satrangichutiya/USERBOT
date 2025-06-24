"""
User info plugin
Commands: inf, inffull, sgb
"""

import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied
from config import Config
from utils.helpers import edit_or_reply, extract_user_info

@Client.on_message(filters.command(["inf", "info"], Config.COMMAND_PREFIXES) & filters.me)
async def user_info(client: Client, message: Message):
    """Get basic user information"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            user = message.from_user
    else:
        try:
            if user_id:
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(username)
        except (PeerIdInvalid, UsernameNotOccupied):
            await edit_or_reply(message, "❌ **User not found!**")
            return
        except Exception as e:
            await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")
            return
    
    if not user:
        await edit_or_reply(message, "❌ **User not found!**")
        return
    
    # Get user photos count
    try:
        photos = await client.get_chat_photos_count(user.id)
    except:
        photos = 0
    
    # Get common chats count
    try:
        common_chats = await client.get_common_chats(user.id)
        common_count = len(common_chats)
    except:
        common_count = 0
    
    user_info_text = (
        f"👤 **User Information**\n\n"
        f"**Name:** {user.first_name}"
    )
    
    if user.last_name:
        user_info_text += f" {user.last_name}"
    
    user_info_text += f"\n**User ID:** `{user.id}`"
    
    if user.username:
        user_info_text += f"\n**Username:** @{user.username}"
    
    if user.phone_number:
        user_info_text += f"\n**Phone:** `{user.phone_number}`"
    
    user_info_text += (
        f"\n**Is Bot:** {'Yes' if user.is_bot else 'No'}"
        f"\n**Is Verified:** {'Yes' if user.is_verified else 'No'}"
        f"\n**Is Premium:** {'Yes' if user.is_premium else 'No'}"
        f"\n**Is Scam:** {'Yes' if user.is_scam else 'No'}"
        f"\n**Is Fake:** {'Yes' if user.is_fake else 'No'}"
        f"\n**Photos Count:** `{photos}`"
        f"\n**Common Chats:** `{common_count}`"
    )
    
    if user.status:
        if user.status == "online":
            user_info_text += f"\n**Status:** 🟢 Online"
        elif user.status == "offline":
            user_info_text += f"\n**Status:** ⚫ Offline"
        elif user.status == "recently":
            user_info_text += f"\n**Status:** 🟡 Recently"
        elif user.status == "within_week":
            user_info_text += f"\n**Status:** 🟠 Within a week"
        elif user.status == "within_month":
            user_info_text += f"\n**Status:** 🔴 Within a month"
        elif user.status == "long_time_ago":
            user_info_text += f"\n**Status:** ⚫ Long time ago"
    
    # Get profile photo
    try:
        if photos > 0:
            photo = await client.download_media(
                await client.get_chat_photos(user.id, limit=1).__anext__(),
                in_memory=True
            )
            await message.reply_photo(photo, caption=user_info_text)
            await message.delete()
        else:
            await edit_or_reply(message, user_info_text)
    except:
        await edit_or_reply(message, user_info_text)

@Client.on_message(filters.command(["inffull", "fullinfo"], Config.COMMAND_PREFIXES) & filters.me)
async def full_user_info(client: Client, message: Message):
    """Get detailed user information"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            user = message.from_user
    else:
        try:
            if user_id:
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(username)
        except (PeerIdInvalid, UsernameNotOccupied):
            await edit_or_reply(message, "❌ **User not found!**")
            return
        except Exception as e:
            await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")
            return
    
    if not user:
        await edit_or_reply(message, "❌ **User not found!**")
        return
    
    # Get detailed information
    try:
        photos = await client.get_chat_photos_count(user.id)
        common_chats = await client.get_common_chats(user.id)
        common_count = len(common_chats)
        
        # Get user's chat info if available
        try:
            chat_info = await client.get_chat(user.id)
            bio = chat_info.bio if hasattr(chat_info, 'bio') else None
        except:
            bio = None
        
        full_info = (
            f"👤 **Detailed User Information**\n\n"
            f"**Full Name:** {user.first_name}"
        )
        
        if user.last_name:
            full_info += f" {user.last_name}"
        
        full_info += (
            f"\n**User ID:** `{user.id}`"
            f"\n**Username:** @{user.username}" if user.username else "\n**Username:** None"
        )
        
        if user.phone_number:
            full_info += f"\n**Phone Number:** `{user.phone_number}`"
        
        if bio:
            full_info += f"\n**Bio:** {bio}"
        
        full_info += (
            f"\n**Account Type:** {'Bot' if user.is_bot else 'User'}"
            f"\n**Verified:** {'✅ Yes' if user.is_verified else '❌ No'}"
            f"\n**Premium:** {'✅ Yes' if user.is_premium else '❌ No'}"
            f"\n**Scam:** {'⚠️ Yes' if user.is_scam else '✅ No'}"
            f"\n**Fake:** {'⚠️ Yes' if user.is_fake else '✅ No'}"
            f"\n**Restricted:** {'⚠️ Yes' if user.is_restricted else '✅ No'}"
            f"\n**Deleted:** {'⚠️ Yes' if user.is_deleted else '✅ No'}"
            f"\n**Profile Photos:** `{photos}`"
            f"\n**Common Chats:** `{common_count}`"
        )
        
        # Add status information
        if user.status:
            status_map = {
                "online": "🟢 Online",
                "offline": "⚫ Offline", 
                "recently": "🟡 Recently",
                "within_week": "🟠 Within a week",
                "within_month": "🔴 Within a month",
                "long_time_ago": "⚫ Long time ago"
            }
            full_info += f"\n**Last Seen:** {status_map.get(user.status, user.status)}"
        
        # Add language code if available
        if hasattr(user, 'language_code') and user.language_code:
            full_info += f"\n**Language:** `{user.language_code}`"
        
        # List some common chats
        if common_count > 0:
            full_info += f"\n\n**Common Chats ({min(5, common_count)}):**"
            for i, chat in enumerate(common_chats[:5]):
                full_info += f"\n• {chat.title}"
        
        await edit_or_reply(message, full_info)
        
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error getting full info:** `{str(e)}`")

@Client.on_message(filters.command(["sgb", "sangmata"], Config.COMMAND_PREFIXES) & filters.me)
async def sangmata_info(client: Client, message: Message):
    """Get Sangmata-style user history (simulated)"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
            return
    else:
        try:
            if user_id:
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(username)
        except (PeerIdInvalid, UsernameNotOccupied):
            await edit_or_reply(message, "❌ **User not found!**")
            return
        except Exception as e:
            await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")
            return
    
    if not user:
        await edit_or_reply(message, "❌ **User not found!**")
        return
    
    # Simulate Sangmata-style response
    sangmata_text = (
        f"🔍 **Sangmata History for {user.first_name}**\n\n"
        f"**User ID:** `{user.id}`\n"
        f"**Current Name:** {user.first_name}"
    )
    
    if user.last_name:
        sangmata_text += f" {user.last_name}"
    
    if user.username:
        sangmata_text += f"\n**Current Username:** @{user.username}"
    
    sangmata_text += (
        f"\n\n**📊 Account Statistics:**\n"
        f"• **Account Age:** Estimated\n"
        f"• **Profile Changes:** Unknown\n"
        f"• **Username Changes:** Unknown\n"
        f"• **Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"*Note: This is a simulated response. Real Sangmata data requires API access.*"
    )
    
    await edit_or_reply(message, sangmata_text)