"""
Admin commands plugin
Commands: ban, unban, kick, mute, unmute, pin, unpin, purge, del
"""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid, FloodWait
from config import Config
from utils.helpers import edit_or_reply, extract_user_info

@Client.on_message(filters.command(["ban"], Config.COMMAND_PREFIXES) & filters.me)
async def ban_user(client: Client, message: Message):
    """Ban a user from the chat"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    try:
        if user_id:
            await client.ban_chat_member(message.chat.id, user_id)
            user_mention = f"User {user_id}"
        else:
            await client.ban_chat_member(message.chat.id, username)
            user_mention = f"@{username}"
        
        await edit_or_reply(message, f"🔨 **Banned {user_mention} successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to ban users!**")
    except UserAdminInvalid:
        await edit_or_reply(message, "❌ **Cannot ban admin users!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["unban"], Config.COMMAND_PREFIXES) & filters.me)
async def unban_user(client: Client, message: Message):
    """Unban a user from the chat"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    try:
        if user_id:
            await client.unban_chat_member(message.chat.id, user_id)
            user_mention = f"User {user_id}"
        else:
            await client.unban_chat_member(message.chat.id, username)
            user_mention = f"@{username}"
        
        await edit_or_reply(message, f"✅ **Unbanned {user_mention} successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to unban users!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["kick"], Config.COMMAND_PREFIXES) & filters.me)
async def kick_user(client: Client, message: Message):
    """Kick a user from the chat"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    try:
        if user_id:
            await client.ban_chat_member(message.chat.id, user_id)
            await client.unban_chat_member(message.chat.id, user_id)
            user_mention = f"User {user_id}"
        else:
            await client.ban_chat_member(message.chat.id, username)
            await client.unban_chat_member(message.chat.id, username)
            user_mention = f"@{username}"
        
        await edit_or_reply(message, f"👢 **Kicked {user_mention} successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to kick users!**")
    except UserAdminInvalid:
        await edit_or_reply(message, "❌ **Cannot kick admin users!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["mute"], Config.COMMAND_PREFIXES) & filters.me)
async def mute_user(client: Client, message: Message):
    """Mute a user in the chat"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    try:
        permissions = ChatPermissions(can_send_messages=False)
        
        if user_id:
            await client.restrict_chat_member(message.chat.id, user_id, permissions)
            user_mention = f"User {user_id}"
        else:
            await client.restrict_chat_member(message.chat.id, username, permissions)
            user_mention = f"@{username}"
        
        await edit_or_reply(message, f"🔇 **Muted {user_mention} successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to mute users!**")
    except UserAdminInvalid:
        await edit_or_reply(message, "❌ **Cannot mute admin users!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["unmute"], Config.COMMAND_PREFIXES) & filters.me)
async def unmute_user(client: Client, message: Message):
    """Unmute a user in the chat"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False
        )
        
        if user_id:
            await client.restrict_chat_member(message.chat.id, user_id, permissions)
            user_mention = f"User {user_id}"
        else:
            await client.restrict_chat_member(message.chat.id, username, permissions)
            user_mention = f"@{username}"
        
        await edit_or_reply(message, f"🔊 **Unmuted {user_mention} successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to unmute users!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["pin"], Config.COMMAND_PREFIXES) & filters.me)
async def pin_message(client: Client, message: Message):
    """Pin a message"""
    if not message.reply_to_message:
        await edit_or_reply(message, "❌ **Please reply to a message to pin it!**")
        return
    
    try:
        await client.pin_chat_message(message.chat.id, message.reply_to_message.id)
        await edit_or_reply(message, "📌 **Message pinned successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to pin messages!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["unpin"], Config.COMMAND_PREFIXES) & filters.me)
async def unpin_message(client: Client, message: Message):
    """Unpin a message"""
    try:
        if message.reply_to_message:
            await client.unpin_chat_message(message.chat.id, message.reply_to_message.id)
        else:
            await client.unpin_chat_message(message.chat.id)
        
        await edit_or_reply(message, "📌 **Message unpinned successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to unpin messages!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["purge"], Config.COMMAND_PREFIXES) & filters.me)
async def purge_messages(client: Client, message: Message):
    """Delete messages from replied message to current message"""
    if not message.reply_to_message:
        await edit_or_reply(message, "❌ **Please reply to a message to start purging from!**")
        return
    
    try:
        start_id = message.reply_to_message.id
        end_id = message.id
        
        message_ids = list(range(start_id, end_id + 1))
        
        # Delete messages in batches
        deleted_count = 0
        for i in range(0, len(message_ids), 100):
            batch = message_ids[i:i+100]
            try:
                await client.delete_messages(message.chat.id, batch)
                deleted_count += len(batch)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await client.delete_messages(message.chat.id, batch)
                deleted_count += len(batch)
            except:
                pass
        
        result_msg = await client.send_message(
            message.chat.id,
            f"🗑️ **Purged {deleted_count} messages successfully!**"
        )
        
        # Delete the result message after 3 seconds
        await asyncio.sleep(3)
        await result_msg.delete()
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to delete messages!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["del", "delete"], Config.COMMAND_PREFIXES) & filters.me)
async def delete_message(client: Client, message: Message):
    """Delete replied message"""
    if not message.reply_to_message:
        await message.delete()
        return
    
    try:
        await message.reply_to_message.delete()
        await message.delete()
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["promote"], Config.COMMAND_PREFIXES) & filters.me)
async def promote_user(client: Client, message: Message):
    """Promote a user to admin"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    try:
        if user_id:
            await client.promote_chat_member(
                message.chat.id,
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True
                )
            )
            user_mention = f"User {user_id}"
        else:
            await client.promote_chat_member(
                message.chat.id,
                username,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True
                )
            )
            user_mention = f"@{username}"
        
        await edit_or_reply(message, f"⬆️ **Promoted {user_mention} to admin successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to promote users!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["demote"], Config.COMMAND_PREFIXES) & filters.me)
async def demote_user(client: Client, message: Message):
    """Demote an admin user"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    try:
        if user_id:
            await client.promote_chat_member(
                message.chat.id,
                user_id,
                privileges=ChatPrivileges()
            )
            user_mention = f"User {user_id}"
        else:
            await client.promote_chat_member(
                message.chat.id,
                username,
                privileges=ChatPrivileges()
            )
            user_mention = f"@{username}"
        
        await edit_or_reply(message, f"⬇️ **Demoted {user_mention} successfully!**")
    
    except ChatAdminRequired:
        await edit_or_reply(message, "❌ **I need admin rights to demote users!**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")