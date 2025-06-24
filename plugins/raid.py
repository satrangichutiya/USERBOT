"""
Raid plugin - Advanced raiding features
Commands: raid, raidstop, spam, draid
"""

import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.helpers import edit_or_reply, extract_user_info

# Raid storage
active_raids = {}
raid_messages = [
    "🔥 RAID ACTIVATED! 🔥",
    "💀 GET READY FOR CHAOS! 💀",
    "⚡ LIGHTNING STRIKE! ⚡",
    "🌪️ TORNADO INCOMING! 🌪️",
    "💥 BOOM! HEADSHOT! 💥",
    "🎯 TARGET ACQUIRED! 🎯",
    "🚀 ROCKET LAUNCHER! 🚀",
    "⚔️ SWORD ATTACK! ⚔️",
    "🔫 MACHINE GUN FIRE! 🔫",
    "💣 BOMB EXPLOSION! 💣",
    "🌋 VOLCANIC ERUPTION! 🌋",
    "❄️ ICE STORM! ❄️",
    "🌊 TSUNAMI WAVE! 🌊",
    "🔥 FIRE STORM! 🔥",
    "⚡ THUNDER BOLT! ⚡"
]

love_messages = [
    "❤️ I LOVE YOU SO MUCH! ❤️",
    "💕 YOU'RE MY EVERYTHING! 💕",
    "💖 MY HEART BEATS FOR YOU! 💖",
    "🌹 YOU'RE SO BEAUTIFUL! 🌹",
    "💝 YOU'RE MY TREASURE! 💝",
    "🥰 I'M CRAZY ABOUT YOU! 🥰",
    "😍 YOU'RE AMAZING! 😍",
    "💘 LOVE AT FIRST SIGHT! 💘",
    "💓 MY HEART IS YOURS! 💓",
    "🌟 YOU'RE MY STAR! 🌟",
    "🦋 YOU GIVE ME BUTTERFLIES! 🦋",
    "🌈 YOU'RE MY RAINBOW! 🌈",
    "🎵 YOU'RE MY SONG! 🎵",
    "🌙 YOU'RE MY MOON! 🌙",
    "☀️ YOU'RE MY SUNSHINE! ☀️"
]

gali_messages = [
    "🤬 TERE BAAP KA KAAM HAI KYA?",
    "😠 DIMAG GHAR PE BHOOL AAYA?",
    "🙄 BUDDHU KAHIN KA!",
    "😤 PAGAL HAI KYA TU?",
    "🤦‍♂️ ULLU KE PATTHE!",
    "😡 BEVAKOOF INSAAN!",
    "🤯 TERA DIMAG KHARAB HAI!",
    "😠 GADHE JAISA DIMAAG!",
    "🤬 NALAYAK INSAAN!",
    "😤 BEWAKOOF KI AULAD!",
    "🙄 PAAGAL KUTTA!",
    "😡 MENTAL HAI KYA?",
    "🤦‍♂️ JAAHIL INSAAN!",
    "😠 MOORAKH HAI TU!",
    "🤬 ANDHA HAI KYA?"
]

@Client.on_message(filters.command(["raid"], Config.COMMAND_PREFIXES) & filters.me)
async def start_raid(client: Client, message: Message):
    """Start raid on a user"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username to raid!**")
        return
    
    # Get raid count (default 10)
    count = 10
    if len(message.command) > 2:
        try:
            count = int(message.command[2])
            if count > 50:
                count = 50  # Limit to prevent spam
        except:
            count = 10
    
    try:
        if user_id:
            target_user = await client.get_users(user_id)
        else:
            target_user = await client.get_users(username)
        
        target_id = target_user.id
        target_name = target_user.first_name
        
        # Check if raid is already active
        if target_id in active_raids:
            await edit_or_reply(message, f"⚠️ **Raid already active on {target_name}!**")
            return
        
        # Start raid
        active_raids[target_id] = True
        await edit_or_reply(message, f"🔥 **Starting raid on {target_name}!**\n**Count:** `{count}`")
        
        # Send raid messages
        for i in range(count):
            if target_id not in active_raids:  # Check if raid was stopped
                break
            
            try:
                raid_msg = random.choice(raid_messages)
                await client.send_message(target_id, f"{raid_msg}\n\n**Raid #{i+1}** by 🌙 Moon UserBot")
                await asyncio.sleep(1)  # 1 second delay
            except Exception as e:
                if "blocked" in str(e).lower():
                    await message.reply(f"❌ **Raid stopped: Blocked by {target_name}**")
                    break
                elif "flood" in str(e).lower():
                    await asyncio.sleep(5)  # Wait for flood limit
                    continue
        
        # Remove from active raids
        if target_id in active_raids:
            del active_raids[target_id]
        
        await message.reply(f"✅ **Raid completed on {target_name}!**")
    
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["raidstop"], Config.COMMAND_PREFIXES) & filters.me)
async def stop_raid(client: Client, message: Message):
    """Stop active raid"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        # Stop all raids
        if active_raids:
            active_raids.clear()
            await edit_or_reply(message, "🛑 **All raids stopped!**")
        else:
            await edit_or_reply(message, "❌ **No active raids to stop!**")
        return
    
    try:
        if user_id:
            target_user = await client.get_users(user_id)
        else:
            target_user = await client.get_users(username)
        
        target_id = target_user.id
        target_name = target_user.first_name
        
        if target_id in active_raids:
            del active_raids[target_id]
            await edit_or_reply(message, f"🛑 **Raid stopped on {target_name}!**")
        else:
            await edit_or_reply(message, f"❌ **No active raid on {target_name}!**")
    
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["spam"], Config.COMMAND_PREFIXES) & filters.me)
async def spam_message(client: Client, message: Message):
    """Spam a message"""
    if len(message.command) < 3:
        await edit_or_reply(message, "❌ **Usage:** `.spam [count] [message]`")
        return
    
    try:
        count = int(message.command[1])
        if count > 20:
            count = 20  # Limit spam count
        
        spam_text = " ".join(message.command[2:])
        
        await edit_or_reply(message, f"📢 **Spamming {count} times...**")
        
        for i in range(count):
            try:
                await client.send_message(message.chat.id, f"{spam_text}")
                await asyncio.sleep(0.5)  # Small delay
            except Exception as e:
                if "flood" in str(e).lower():
                    await asyncio.sleep(5)
                    continue
                else:
                    break
        
        await client.send_message(message.chat.id, f"✅ **Spam completed! Sent {count} messages.**")
    
    except ValueError:
        await edit_or_reply(message, "❌ **Invalid count! Please provide a number.**")
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["draid", "delayraid"], Config.COMMAND_PREFIXES) & filters.me)
async def delay_raid(client: Client, message: Message):
    """Start delayed raid"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    # Get parameters
    count = 5
    delay = 10
    
    if len(message.command) > 2:
        try:
            count = int(message.command[2])
            if count > 20:
                count = 20
        except:
            pass
    
    if len(message.command) > 3:
        try:
            delay = int(message.command[3])
            if delay > 60:
                delay = 60
        except:
            pass
    
    try:
        if user_id:
            target_user = await client.get_users(user_id)
        else:
            target_user = await client.get_users(username)
        
        target_id = target_user.id
        target_name = target_user.first_name
        
        await edit_or_reply(message, 
            f"⏰ **Delayed raid scheduled!**\n"
            f"**Target:** {target_name}\n"
            f"**Count:** {count}\n"
            f"**Delay:** {delay} seconds"
        )
        
        # Wait for delay
        await asyncio.sleep(delay)
        
        # Start raid
        active_raids[target_id] = True
        
        for i in range(count):
            if target_id not in active_raids:
                break
            
            try:
                raid_msg = random.choice(raid_messages)
                await client.send_message(target_id, f"⏰ **DELAYED RAID!** ⏰\n\n{raid_msg}")
                await asyncio.sleep(2)
            except Exception as e:
                if "blocked" in str(e).lower():
                    break
                elif "flood" in str(e).lower():
                    await asyncio.sleep(5)
                    continue
        
        if target_id in active_raids:
            del active_raids[target_id]
    
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["loveraid"], Config.COMMAND_PREFIXES) & filters.me)
async def love_raid(client: Client, message: Message):
    """Start love raid"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    count = 10
    if len(message.command) > 2:
        try:
            count = int(message.command[2])
            if count > 30:
                count = 30
        except:
            pass
    
    try:
        if user_id:
            target_user = await client.get_users(user_id)
        else:
            target_user = await client.get_users(username)
        
        target_id = target_user.id
        target_name = target_user.first_name
        
        await edit_or_reply(message, f"💕 **Starting love raid on {target_name}!**")
        
        active_raids[target_id] = True
        
        for i in range(count):
            if target_id not in active_raids:
                break
            
            try:
                love_msg = random.choice(love_messages)
                await client.send_message(target_id, f"{love_msg}\n\n💕 **Love Raid #{i+1}** 💕")
                await asyncio.sleep(1.5)
            except Exception as e:
                if "blocked" in str(e).lower():
                    break
                elif "flood" in str(e).lower():
                    await asyncio.sleep(5)
                    continue
        
        if target_id in active_raids:
            del active_raids[target_id]
        
        await message.reply(f"💕 **Love raid completed on {target_name}!**")
    
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["galiraid"], Config.COMMAND_PREFIXES) & filters.me)
async def gali_raid(client: Client, message: Message):
    """Start gali raid"""
    user_id, username = extract_user_info(message)
    
    if not user_id and not username:
        await edit_or_reply(message, "❌ **Please reply to a user or provide user ID/username!**")
        return
    
    count = 8
    if len(message.command) > 2:
        try:
            count = int(message.command[2])
            if count > 15:
                count = 15
        except:
            pass
    
    try:
        if user_id:
            target_user = await client.get_users(user_id)
        else:
            target_user = await client.get_users(username)
        
        target_id = target_user.id
        target_name = target_user.first_name
        
        await edit_or_reply(message, f"🤬 **Starting gali raid on {target_name}!**")
        
        active_raids[target_id] = True
        
        for i in range(count):
            if target_id not in active_raids:
                break
            
            try:
                gali_msg = random.choice(gali_messages)
                await client.send_message(target_id, f"{gali_msg}\n\n🤬 **Gali Raid #{i+1}** 🤬")
                await asyncio.sleep(2)
            except Exception as e:
                if "blocked" in str(e).lower():
                    break
                elif "flood" in str(e).lower():
                    await asyncio.sleep(5)
                    continue
        
        if target_id in active_raids:
            del active_raids[target_id]
        
        await message.reply(f"🤬 **Gali raid completed on {target_name}!**")
    
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["raidstatus"], Config.COMMAND_PREFIXES) & filters.me)
async def raid_status(client: Client, message: Message):
    """Show active raids status"""
    if not active_raids:
        await edit_or_reply(message, "✅ **No active raids!**")
        return
    
    status_text = f"🔥 **Active Raids ({len(active_raids)}):**\n\n"
    
    for target_id in active_raids:
        try:
            user = await client.get_users(target_id)
            status_text += f"• {user.first_name} (`{target_id}`)\n"
        except:
            status_text += f"• User `{target_id}`\n"
    
    status_text += f"\n**Commands:**\n"
    status_text += f"• `.raidstop` - Stop all raids\n"
    status_text += f"• `.raidstop [user]` - Stop specific raid"
    
    await edit_or_reply(message, status_text)