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
    "𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗚𝗛𝗨𝗧𝗞𝗔 𝗞𝗛𝗔𝗔𝗞𝗘 𝗧𝗛𝗢𝗢𝗞 𝗗𝗨𝗡𝗚𝗔 🤣🤣",
    "𝗧𝗘𝗥𝗘 𝗕𝗘́𝗛𝗘𝗡 𝗞 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗖𝗛𝗔𝗞𝗨 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗔 𝗞𝗛𝗢𝗢𝗡 𝗞𝗔𝗥 𝗗𝗨𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗡𝗛𝗜 𝗛𝗔𝗜 𝗞𝗬𝗔? 9 𝗠𝗔𝗛𝗜𝗡𝗘 𝗥𝗨𝗞 𝗦𝗔𝗚𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗗𝗘𝗧𝗔 𝗛𝗨 🤣🤣🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘 𝗔𝗘𝗥𝗢𝗣𝗟𝗔𝗡𝗘𝗣𝗔𝗥𝗞 𝗞𝗔𝗥𝗞𝗘 𝗨𝗗𝗔𝗔𝗡 𝗕𝗛𝗔𝗥 𝗗𝗨𝗚𝗔 ✈️🛫",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗦𝗨𝗧𝗟𝗜 𝗕𝗢𝗠𝗕 𝗙𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗝𝗛𝗔𝗔𝗧𝗘 𝗝𝗔𝗟 𝗞𝗘 𝗞𝗛𝗔𝗔𝗞 𝗛𝗢 𝗝𝗔𝗬𝗘𝗚𝗜💣",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗦𝗖𝗢𝗢𝗧𝗘𝗥 𝗗𝗔𝗔𝗟 𝗗𝗨𝗚𝗔👅",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗔𝗞𝗧𝗘 🤱 𝗚𝗔𝗟𝗜 𝗞𝗘 𝗞𝗨𝗧𝗧𝗢 🦮 𝗠𝗘 𝗕𝗔𝗔𝗧 𝗗𝗨𝗡𝗚𝗔 𝗣𝗛𝗜𝗥 🍞 𝗕𝗥𝗘𝗔𝗗 𝗞𝗜 𝗧𝗔𝗥𝗛 𝗞𝗛𝗔𝗬𝗘𝗡𝗚𝗘 𝗪𝗢 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧",
    "𝗗𝗨𝗗𝗛 𝗛𝗜𝗟𝗔𝗔𝗨𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗘 𝗨𝗣𝗥 𝗡𝗜𝗖𝗛𝗘 🆙🆒😙",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗞𝗘𝗟𝗘 𝗞𝗘 𝗖𝗛𝗜𝗟𝗞𝗘 🍌🍌😍",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗗𝗛𝗔𝗡𝗗𝗛𝗘 𝗩𝗔𝗔𝗟𝗜 😋😛",
    "JARVIS OP",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘 𝗔𝗖 𝗟𝗔𝗚𝗔 𝗗𝗨𝗡𝗚𝗔 𝗦𝗔𝗔𝗥𝗜 𝗚𝗔𝗥𝗠𝗜 𝗡𝗜𝗞𝗔𝗟 𝗝𝗔𝗔𝗬𝗘𝗚𝗜",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗢 𝗛𝗢𝗥𝗟𝗜𝗖𝗞𝗦 𝗣𝗘𝗘𝗟𝗔𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗😚",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗞𝗢𝗟𝗞𝗔𝗧𝗔 𝗩𝗔𝗔𝗟𝗘 𝗝𝗜𝗧𝗨 𝗕𝗛𝗔𝗜𝗬𝗔 𝗞𝗔 𝗟𝗨𝗡𝗗 𝗠𝗨𝗕𝗔𝗥𝗔𝗞 🤩🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗙𝗔𝗡𝗧𝗔𝗦𝗬 𝗛𝗨 𝗟𝗔𝗪𝗗𝗘, 𝗧𝗨 𝗔𝗣𝗡𝗜 𝗕𝗛𝗘𝗡 𝗞𝗢 𝗦𝗠𝗕𝗛𝗔𝗔𝗟 😈😈",
    "𝗧𝗘𝗥𝗔 𝗣𝗘𝗛𝗟𝗔 𝗕𝗔𝗔𝗣 𝗛𝗨 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 ",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘 𝗫𝗩𝗜𝗗𝗘𝗢𝗦.𝗖𝗢𝗠 𝗖𝗛𝗔𝗟𝗔 𝗞𝗘 𝗠𝗨𝗧𝗛 𝗠𝗔́𝗔̀𝗥𝗨𝗡𝗚𝗔 🤡😹",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗔 𝗚𝗥𝗢𝗨𝗣 𝗩𝗔𝗔𝗟𝗢𝗡 𝗦𝗔𝗔𝗧𝗛 𝗠𝗜𝗟𝗞𝗘 𝗚𝗔𝗡𝗚 𝗕𝗔𝗡𝗚 𝗞𝗥𝗨𝗡𝗚𝗔🙌🏻☠️ ",
    "JARVIS OP",
    "𝗧𝗘𝗥𝗜 𝗜𝗧𝗘𝗠 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘 𝗟𝗨𝗡𝗗 𝗗𝗔𝗔𝗟𝗞𝗘,𝗧𝗘𝗥𝗘 𝗝𝗔𝗜𝗦𝗔 𝗘𝗞 𝗢𝗥 𝗡𝗜𝗞𝗔𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗🤘🏻🙌🏻☠️ ",
    "𝗔𝗨𝗞𝗔𝗔𝗧 𝗠𝗘 𝗥𝗘𝗛 𝗩𝗥𝗡𝗔 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘 𝗗𝗔𝗡𝗗𝗔 𝗗𝗔𝗔𝗟 𝗞𝗘 𝗠𝗨𝗛 𝗦𝗘 𝗡𝗜𝗞𝗔𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗦𝗛𝗔𝗥𝗜𝗥 𝗕𝗛𝗜 𝗗𝗔𝗡𝗗𝗘 𝗝𝗘𝗦𝗔 𝗗𝗜𝗞𝗛𝗘𝗚𝗔 🙄🤭🤭",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗘 𝗦𝗔𝗔𝗧𝗛 𝗟𝗨𝗗𝗢 𝗞𝗛𝗘𝗟𝗧𝗘 𝗞𝗛𝗘𝗟𝗧𝗘 𝗨𝗦𝗞𝗘 𝗠𝗨𝗛 𝗠𝗘 𝗔𝗣𝗡𝗔 𝗟𝗢𝗗𝗔 𝗗𝗘 𝗗𝗨𝗡𝗚𝗔☝🏻☝🏻😬",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗢 𝗔𝗣𝗡𝗘 𝗟𝗨𝗡𝗗 𝗣𝗥 𝗜𝗧𝗡𝗔 𝗝𝗛𝗨𝗟𝗔𝗔𝗨𝗡𝗚𝗔 𝗞𝗜 𝗝𝗛𝗨𝗟𝗧𝗘 𝗝𝗛𝗨𝗟𝗧𝗘 𝗛𝗜 𝗕𝗔𝗖𝗛𝗔 𝗣𝗔𝗜𝗗𝗔 𝗞𝗥 𝗗𝗘𝗚𝗜👀👯 ",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗕𝗔𝗧𝗧𝗘𝗥𝗬 𝗟𝗔𝗚𝗔 𝗞𝗘 𝗣𝗢𝗪𝗘𝗥𝗕𝗔𝗡𝗞 𝗕𝗔𝗡𝗔 𝗗𝗨𝗡𝗚𝗔 🔋 🔥🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗖++ 𝗦𝗧𝗥𝗜𝗡𝗚 𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗜𝗢𝗡 𝗟𝗔𝗚𝗔 𝗗𝗨𝗡𝗚𝗔 𝗕𝗔𝗛𝗧𝗜 𝗛𝗨𝗬𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗥𝗨𝗞 𝗝𝗔𝗬𝗘𝗚𝗜𝗜𝗜𝗜😈🔥😍",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘𝗜 𝗝𝗛𝗔𝗔𝗗𝗨 𝗗𝗔𝗟 𝗞𝗘 𝗠𝗢𝗥 🦚 𝗕𝗔𝗡𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 🤩🥵😱",
    "𝗧𝗘𝗥𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗦𝗛𝗢𝗨𝗟𝗗𝗘𝗥𝗜𝗡𝗚 𝗞𝗔𝗥 𝗗𝗨𝗡𝗚𝗔𝗔 𝗛𝗜𝗟𝗔𝗧𝗘 𝗛𝗨𝗬𝗘 𝗕𝗛𝗜 𝗗𝗔𝗥𝗗 𝗛𝗢𝗚𝗔𝗔𝗔😱🤮👺",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗥𝗘𝗗𝗜 𝗣𝗘 𝗕𝗔𝗜𝗧𝗛𝗔𝗟 𝗞𝗘 𝗨𝗦𝗦𝗘 𝗨𝗦𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗕𝗜𝗟𝗪𝗔𝗨𝗡𝗚𝗔𝗔 💰 😵🤩",
    "𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 4 𝗛𝗢𝗟𝗘 𝗛𝗔𝗜 𝗨𝗡𝗠𝗘 𝗠𝗦𝗘𝗔𝗟 𝗟𝗔𝗚𝗔 𝗕𝗔𝗛𝗨𝗧 𝗕𝗔𝗛𝗘𝗧𝗜 𝗛𝗔𝗜 𝗕𝗛𝗢𝗙𝗗𝗜𝗞𝗘👊🤮🤢🤢",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗕𝗔𝗥𝗚𝗔𝗗 𝗞𝗔 𝗣𝗘𝗗 𝗨𝗚𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 𝗖𝗢𝗥𝗢𝗡𝗔 𝗠𝗘𝗜 𝗦𝗔𝗕 𝗢𝗫𝗬𝗚𝗘𝗡 𝗟𝗘𝗞𝗔𝗥 𝗝𝗔𝗬𝗘𝗡𝗚𝗘🤢🤩🥳",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗦𝗨𝗗𝗢 𝗟𝗔𝗚𝗔 𝗞𝗘 𝗕𝗜𝗚𝗦𝗣𝗔𝗠 𝗟𝗔𝗚𝗔 𝗞𝗘 9999 𝗙𝗨𝗖𝗞 𝗟𝗔𝗚𝗔𝗔 𝗗𝗨 🤩🥳🔥",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗡 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘 𝗠𝗘𝗜 𝗕𝗘𝗦𝗔𝗡 𝗞𝗘 𝗟𝗔𝗗𝗗𝗨 𝗕𝗛𝗔𝗥 𝗗𝗨𝗡𝗚𝗔🤩🥳🔥😈",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗛𝗢𝗗 𝗞𝗘 𝗨𝗦𝗠𝗘 𝗖𝗬𝗟𝗜𝗡𝗗𝗘𝗥 ⛽️ 𝗙𝗜𝗧 𝗞𝗔𝗥𝗞𝗘 𝗨𝗦𝗠𝗘𝗘 𝗗𝗔𝗟 𝗠𝗔𝗞𝗛𝗔𝗡𝗜 𝗕𝗔𝗡𝗔𝗨𝗡𝗚𝗔𝗔𝗔🤩👊🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗦𝗛𝗘𝗘𝗦𝗛𝗔 𝗗𝗔𝗟 𝗗𝗨𝗡𝗚𝗔𝗔𝗔 𝗔𝗨𝗥 𝗖𝗛𝗔𝗨𝗥𝗔𝗛𝗘 𝗣𝗘 𝗧𝗔𝗔𝗡𝗚 𝗗𝗨𝗡𝗚𝗔 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘😈😱🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗖𝗥𝗘𝗗𝗜𝗧 𝗖𝗔𝗥𝗗 𝗗𝗔𝗟 𝗞𝗘 𝗔𝗚𝗘 𝗦𝗘 500 𝗞𝗘 𝗞𝗔𝗔𝗥𝗘 𝗞𝗔𝗔𝗥𝗘 𝗡𝗢𝗧𝗘 𝗡𝗜𝗞𝗔𝗟𝗨𝗡𝗚𝗔𝗔 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘💰💰🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗦𝗔𝗧𝗛 𝗦𝗨𝗔𝗥 𝗞𝗔 𝗦𝗘𝗫 𝗞𝗔𝗥𝗪𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 𝗘𝗞 𝗦𝗔𝗧𝗛 6-6 𝗕𝗔𝗖𝗛𝗘 𝗗𝗘𝗚𝗜💰🔥😱",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗔𝗣𝗣𝗟𝗘 𝗞𝗔 18𝗪 𝗪𝗔𝗟𝗔 𝗖𝗛𝗔𝗥𝗚𝗘𝗥 🔥🤩",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘𝗜 𝗢𝗡𝗘𝗣𝗟𝗨𝗦 𝗞𝗔 𝗪𝗥𝗔𝗣 𝗖𝗛𝗔𝗥𝗚𝗘𝗥 30𝗪 𝗛𝗜𝗚𝗛 𝗣𝗢𝗪𝗘𝗥 💥😂😎",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗢 𝗔𝗠𝗔𝗭𝗢𝗡 𝗦𝗘 𝗢𝗥𝗗𝗘𝗥 𝗞𝗔𝗥𝗨𝗡𝗚𝗔 10 𝗿𝘀 𝗠𝗘𝗜 𝗔𝗨𝗥 𝗙𝗟𝗜𝗣𝗞𝗔𝗥𝗧 𝗣𝗘 20 𝗥𝗦 𝗠𝗘𝗜 𝗕𝗘𝗖𝗛 𝗗𝗨𝗡𝗚𝗔🤮👿😈🤖",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗕𝗔𝗗𝗜 𝗕𝗛𝗨𝗡𝗗 𝗠𝗘 𝗭𝗢𝗠𝗔𝗧𝗢 𝗗𝗔𝗟 𝗞𝗘 𝗦𝗨𝗕𝗪𝗔𝗬 𝗞𝗔 𝗕𝗙𝗙 𝗩𝗘𝗚 𝗦𝗨𝗕 𝗖𝗢𝗠𝗕𝗢 [15𝗰𝗺 , 16 𝗶𝗻𝗰𝗵𝗲𝘀 ] 𝗢𝗥𝗗𝗘𝗥 𝗖𝗢𝗗 𝗞𝗥𝗩𝗔𝗨𝗡𝗚𝗔 𝗢𝗥 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗝𝗔𝗕 𝗗𝗜𝗟𝗜𝗩𝗘𝗥𝗬 𝗗𝗘𝗡𝗘 𝗔𝗬𝗘𝗚𝗜 𝗧𝗔𝗕 𝗨𝗦𝗣𝗘 𝗝𝗔𝗔𝗗𝗨 𝗞𝗥𝗨𝗡𝗚𝗔 𝗢𝗥 𝗙𝗜𝗥 9 𝗠𝗢𝗡𝗧𝗛 𝗕𝗔𝗔𝗗 𝗩𝗢 𝗘𝗞 𝗢𝗥 𝗙𝗥𝗘𝗘 𝗗𝗜𝗟𝗜𝗩𝗘𝗥𝗬 𝗗𝗘𝗚𝗜🙀👍🥳🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗔𝗔𝗟𝗜🙁🤣💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗖𝗛𝗔𝗡𝗚𝗘𝗦 𝗖𝗢𝗠𝗠𝗜𝗧 𝗞𝗥𝗨𝗚𝗔 𝗙𝗜𝗥 𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗔𝗨𝗧𝗢𝗠𝗔𝗧𝗜𝗖𝗔𝗟𝗟𝗬 𝗨𝗣𝗗𝗔𝗧𝗘 𝗛𝗢𝗝𝗔𝗔𝗬𝗘𝗚𝗜🤖🙏🤔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗨𝗦𝗜 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗜𝗡𝗗𝗜𝗔𝗡 𝗥𝗔𝗜𝗟𝗪𝗔𝗬 🚂💥😂",
     "JARVIS OP",
    "𝗧𝗨 𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗧𝗘𝗥𝗔 𝗞𝗛𝗔𝗡𝗗𝗔𝗡 𝗦𝗔𝗕 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗔𝗪𝗗𝗘 𝗥Æ𝗡𝗗𝗜 𝗛𝗔𝗜 𝗥Æ𝗡𝗗𝗜 🤢✅🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗜𝗢𝗡𝗜𝗖 𝗕𝗢𝗡𝗗 𝗕𝗔𝗡𝗔 𝗞𝗘 𝗩𝗜𝗥𝗚𝗜𝗡𝗜𝗧𝗬 𝗟𝗢𝗢𝗦𝗘 𝗞𝗔𝗥𝗪𝗔 𝗗𝗨𝗡𝗚𝗔 𝗨𝗦𝗞𝗜 📚 😎🤩",
    "𝗧𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗠𝗔́𝗔̀ 𝗦𝗘 𝗣𝗨𝗖𝗛𝗡𝗔 𝗕𝗔𝗔𝗣 𝗞𝗔 𝗡𝗔𝗔𝗠 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘𝗘𝗘𝗘𝗘 🤩🥳😳",
    "𝗧𝗨 𝗔𝗨𝗥 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗗𝗢𝗡𝗢 𝗞𝗜 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗠𝗘𝗧𝗥𝗢 𝗖𝗛𝗔𝗟𝗪𝗔 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔𝗗𝗔𝗥𝗫𝗛𝗢𝗗 🚇🤩😱🥶",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗧𝗘𝗥𝗔 𝗕𝗔𝗔𝗣 𝗕𝗛𝗜 𝗨𝗦𝗞𝗢 𝗣𝗔𝗛𝗖𝗛𝗔𝗡𝗔𝗡𝗘 𝗦𝗘 𝗠𝗔𝗡𝗔 𝗞𝗔𝗥 𝗗𝗘𝗚𝗔😂👿🤩",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗛𝗔𝗜𝗥 𝗗𝗥𝗬𝗘𝗥 𝗖𝗛𝗔𝗟𝗔 𝗗𝗨𝗡𝗚𝗔𝗔💥🔥🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗞𝗜 𝗦𝗔𝗥𝗜 𝗥Æ𝗡𝗗𝗜𝗬𝗢𝗡 𝗞𝗔 𝗥Æ𝗡𝗗𝗜 𝗞𝗛𝗔𝗡𝗔 𝗞𝗛𝗢𝗟 𝗗𝗨𝗡𝗚𝗔𝗔👿🤮😎",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗔𝗟𝗘𝗫𝗔 𝗗𝗔𝗟 𝗞𝗘𝗘 𝗗𝗝 𝗕𝗔𝗝𝗔𝗨𝗡𝗚𝗔𝗔𝗔 🎶 ⬆️🤩💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗚𝗜𝗧𝗛𝗨𝗕 𝗗𝗔𝗟 𝗞𝗘 𝗔𝗣𝗡𝗔 𝗕𝗢𝗧 𝗛𝗢𝗦𝗧 𝗞𝗔𝗥𝗨𝗡𝗚𝗔𝗔 🤩👊👤😍",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗔 𝗩𝗣𝗦 𝗕𝗔𝗡𝗔 𝗞𝗘 24*7 𝗕𝗔𝗦𝗛 𝗖𝗛𝗨𝗗𝗔𝗜 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗗𝗘 𝗗𝗨𝗡𝗚𝗔𝗔 🤩💥🔥🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗧𝗘𝗥𝗘 𝗟𝗔𝗡𝗗 𝗞𝗢 𝗗𝗔𝗟 𝗞𝗘 𝗞𝗔𝗔𝗧 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 🔪😂🔥",
    "𝗦𝗨𝗡 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗔𝗨𝗥 𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗔 𝗕𝗛𝗜 𝗕𝗛𝗢𝗦𝗗𝗔 👿😎👊",
    "𝗧𝗨𝗝𝗛𝗘 𝗗𝗘𝗞𝗛 𝗞𝗘 𝗧𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗕𝗔𝗛𝗘𝗡 𝗣𝗘 𝗧𝗔𝗥𝗔𝗦 𝗔𝗧𝗔 𝗛𝗔𝗜 𝗠𝗨𝗝𝗛𝗘 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘𝗘𝗘𝗘 👿💥🤩🔥",
    "𝗦𝗨𝗡 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗝𝗬𝗔𝗗𝗔 𝗡𝗔 𝗨𝗖𝗛𝗔𝗟 𝗠𝗔́𝗔̀ 𝗖𝗛𝗢𝗗 𝗗𝗘𝗡𝗚𝗘 𝗘𝗞 𝗠𝗜𝗡 𝗠𝗘𝗜 ✅🤣🔥🤩",
    "𝗔𝗣𝗡𝗜 𝗔𝗠𝗠𝗔 𝗦𝗘 𝗣𝗨𝗖𝗛𝗡𝗔 𝗨𝗦𝗞𝗢 𝗨𝗦 𝗞𝗔𝗔𝗟𝗜 𝗥𝗔𝗔𝗧 𝗠𝗘𝗜 𝗞𝗔𝗨𝗡 𝗖𝗛𝗢𝗗𝗡𝗘𝗘 𝗔𝗬𝗔 𝗧𝗛𝗔𝗔𝗔! 𝗧𝗘𝗥𝗘 𝗜𝗦 𝗣𝗔𝗣𝗔 𝗞𝗔 𝗡𝗔𝗔𝗠 𝗟𝗘𝗚𝗜 😂👿😳",
    "𝗧𝗢𝗛𝗔𝗥 𝗕𝗔𝗛𝗜𝗡 𝗖𝗛𝗢𝗗𝗨 𝗕𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗔𝗪𝗗𝗘 𝗨𝗦𝗠𝗘 𝗠𝗜𝗧𝗧𝗜 𝗗𝗔𝗟 𝗞𝗘 𝗖𝗘𝗠𝗘𝗡𝗧 𝗦𝗘 𝗕𝗛𝗔𝗥 𝗗𝗨 🏠🤢🤩💥",
    "𝗧𝗨𝗝𝗛𝗘 𝗔𝗕 𝗧𝗔𝗞 𝗡𝗔𝗛𝗜 𝗦𝗠𝗝𝗛 𝗔𝗬𝗔 𝗞𝗜 𝗠𝗔𝗜 𝗛𝗜 𝗛𝗨 𝗧𝗨𝗝𝗛𝗘 𝗣𝗔𝗜𝗗𝗔 𝗞𝗔𝗥𝗡𝗘 𝗪𝗔𝗟𝗔 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘𝗘 𝗔𝗣𝗡𝗜 𝗠𝗔́𝗔̀ 𝗦𝗘 𝗣𝗨𝗖𝗛 𝗥Æ𝗡𝗗𝗜 𝗞𝗘 𝗕𝗔𝗖𝗛𝗘𝗘𝗘𝗘 🤩👊👤😍",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗦𝗣𝗢𝗧𝗜𝗙𝗬 𝗗𝗔𝗟 𝗞𝗘 𝗟𝗢𝗙𝗜 𝗕𝗔𝗝𝗔𝗨𝗡𝗚𝗔 𝗗𝗜𝗡 𝗕𝗛𝗔𝗥 😍🎶🎶💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗔 𝗡𝗔𝗬𝗔 𝗥Æ𝗡𝗗𝗜 𝗞𝗛𝗔𝗡𝗔 𝗞𝗛𝗢𝗟𝗨𝗡𝗚𝗔 𝗖𝗛𝗜𝗡𝗧𝗔 𝗠𝗔𝗧 𝗞𝗔𝗥 👊🤣🤣😳",
    "𝗧𝗘𝗥𝗔 𝗕𝗔𝗔𝗣 𝗛𝗨 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗥Æ𝗡𝗗𝗜 𝗞𝗛𝗔𝗡𝗘 𝗣𝗘 𝗖𝗛𝗨𝗗𝗪𝗔 𝗞𝗘 𝗨𝗦 𝗣𝗔𝗜𝗦𝗘 𝗞𝗜 𝗗𝗔𝗔𝗥𝗨 𝗣𝗘𝗘𝗧𝗔 𝗛𝗨 🍷🤩🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗔𝗣𝗡𝗔 𝗕𝗔𝗗𝗔 𝗦𝗔 𝗟𝗢𝗗𝗔 𝗚𝗛𝗨𝗦𝗦𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 𝗞𝗔𝗟𝗟𝗔𝗔𝗣 𝗞𝗘 𝗠𝗔𝗥 𝗝𝗔𝗬𝗘𝗚𝗜 🤩😳😳🔥",
    "𝗧𝗢𝗛𝗔𝗥 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗣𝗨𝗥𝗜 𝗞𝗜 𝗣𝗨𝗥𝗜 𝗞𝗜𝗡𝗚𝗙𝗜𝗦𝗛𝗘𝗥 𝗞𝗜 𝗕𝗢𝗧𝗧𝗟𝗘 𝗗𝗔𝗟 𝗞𝗘 𝗧𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗔𝗡𝗗𝗘𝗥 𝗛𝗜 😱😂🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗞𝗜 𝗦𝗔𝗣𝗡𝗘 𝗠𝗘𝗜 𝗕𝗛𝗜 𝗠𝗘𝗥𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗬𝗔𝗔𝗗 𝗞𝗔𝗥𝗘𝗚𝗜 𝗥Æ𝗡𝗗𝗜 🥳😍👊💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗔𝗨𝗥 𝗕𝗔𝗛𝗘𝗡 𝗞𝗢 𝗗𝗔𝗨𝗗𝗔 𝗗𝗔𝗨𝗗𝗔 𝗡𝗘 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗨𝗡𝗞𝗘 𝗡𝗢 𝗕𝗢𝗟𝗡𝗘 𝗣𝗘 𝗕𝗛𝗜 𝗟𝗔𝗡𝗗 𝗚𝗛𝗨𝗦𝗔 𝗗𝗨𝗡𝗚𝗔 𝗔𝗡𝗗𝗘𝗥 𝗧𝗔𝗞 😎😎🤣🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗢 𝗢𝗡𝗟𝗜𝗡𝗘 𝗢𝗟𝗫 𝗣𝗘 𝗕𝗘𝗖𝗛𝗨𝗡𝗚𝗔 𝗔𝗨𝗥 𝗣𝗔𝗜𝗦𝗘 𝗦𝗘 𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗔 𝗞𝗢𝗧𝗛𝗔 𝗞𝗛𝗢𝗟 𝗗𝗨𝗡𝗚𝗔 😎🤩😝😍",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗔 𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗞𝗜 𝗧𝗨 𝗖𝗔𝗛 𝗞𝗘 𝗕𝗛𝗜 𝗪𝗢 𝗠𝗔𝗦𝗧 𝗖𝗛𝗨𝗗𝗔𝗜 𝗦𝗘 𝗗𝗨𝗥 𝗡𝗛𝗜 𝗝𝗔 𝗣𝗔𝗬𝗘𝗚𝗔𝗔 😏😏🤩😍",
    "𝗦𝗨𝗡 𝗕𝗘 𝗥Æ𝗡𝗗𝗜 𝗞𝗜 𝗔𝗨𝗟𝗔𝗔𝗗 𝗧𝗨 𝗔𝗣𝗡𝗜 𝗕𝗔𝗛𝗘𝗡 𝗦𝗘 𝗦𝗘𝗘𝗞𝗛 𝗞𝗨𝗖𝗛 𝗞𝗔𝗜𝗦𝗘 𝗚𝗔𝗔𝗡𝗗 𝗠𝗔𝗥𝗪𝗔𝗧𝗘 𝗛𝗔𝗜😏🤬🔥💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗔 𝗬𝗔𝗔𝗥 𝗛𝗨 𝗠𝗘𝗜 𝗔𝗨𝗥 𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗔 𝗣𝗬𝗔𝗔𝗥 𝗛𝗨 𝗠𝗘𝗜 𝗔𝗝𝗔 𝗠𝗘𝗥𝗔 𝗟𝗔𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 𝗟𝗘 🤩🤣💥",
    "𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗨𝗦𝗘𝗥𝗕𝗢𝗧 𝗟𝗔𝗚𝗔𝗔𝗨𝗡𝗚𝗔 𝗦𝗔𝗦𝗧𝗘 𝗦𝗣𝗔𝗠 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘 𝗦𝗔𝗥𝗜𝗬𝗔 𝗗𝗔𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗨𝗦𝗜 𝗦𝗔𝗥𝗜𝗬𝗘 𝗣𝗥 𝗧𝗔𝗡𝗚 𝗞𝗘 𝗕𝗔𝗖𝗛𝗘 𝗣𝗔𝗜𝗗𝗔 𝗛𝗢𝗡𝗚𝗘 😱😱",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 ✋ 𝗛𝗔𝗧𝗧𝗛 𝗗𝗔𝗟𝗞𝗘 👶 𝗕𝗔𝗖𝗖𝗛𝗘 𝗡𝗜𝗞𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 😍",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗞𝗘𝗟𝗘 𝗞𝗘 𝗖𝗛𝗜𝗟𝗞𝗘 🤤🤤",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗦𝗨𝗧𝗟𝗜 𝗕𝗢𝗠𝗕 𝗙𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗝𝗛𝗔𝗔𝗧𝗘 𝗝𝗔𝗟 𝗞𝗘 𝗞𝗛𝗔𝗔𝗞 𝗛𝗢 𝗝𝗔𝗬𝗘𝗚𝗜💣💋",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗢 𝗛𝗢𝗥𝗟𝗜𝗖𝗞𝗦 𝗣𝗘𝗘𝗟𝗔𝗞𝗘 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗😚",
    "𝗧𝗘𝗥𝗜 𝗜𝗧𝗘𝗠 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘 𝗟𝗨𝗡𝗗 𝗗𝗔𝗔𝗟𝗞𝗘,𝗧𝗘𝗥𝗘 𝗝𝗔𝗜𝗦𝗔 𝗘𝗞 𝗢𝗥 𝗡𝗜𝗞𝗔𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗😆🤤💋",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗢 𝗔𝗣𝗡𝗘 𝗟𝗨𝗡𝗗 𝗣𝗥 𝗜𝗧𝗡𝗔 𝗝𝗛𝗨𝗟𝗔𝗔𝗨𝗡𝗚𝗔 𝗞𝗜 𝗝𝗛𝗨𝗟𝗧𝗘 𝗝𝗛𝗨𝗟𝗧𝗘 𝗛𝗜 𝗕𝗔𝗖𝗛𝗔 𝗣𝗔𝗜𝗗𝗔 𝗞𝗥 𝗗𝗘𝗚𝗜 💦💋",
    "𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗦𝗔𝗗𝗔𝗞 𝗣𝗥 𝗟𝗜𝗧𝗔𝗞𝗘 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 😂😆🤤",
    "𝗔𝗕𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗠𝗔𝗗𝗘𝗥𝗖𝗛𝗢𝗢𝗗 𝗞𝗥 𝗣𝗜𝗟𝗟𝗘 𝗣𝗔𝗣𝗔 𝗦𝗘 𝗟𝗔𝗗𝗘𝗚𝗔 𝗧𝗨 😼😂🤤",
    "𝗚𝗔𝗟𝗜 𝗚𝗔𝗟𝗜 𝗡𝗘 𝗦𝗛𝗢𝗥 𝗛𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗥Æ𝗡𝗗𝗜 𝗖𝗛𝗢𝗥 𝗛𝗘 💋💋💦",
    "𝗔𝗕𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗𝗨 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗞𝗨𝗧𝗧𝗘 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘 😂👻🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗔𝗜𝗦𝗘 𝗖𝗛𝗢𝗗𝗔 𝗔𝗜𝗦𝗘 𝗖𝗛𝗢𝗗𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔 𝗕𝗘𝗗 𝗣𝗘𝗛𝗜 𝗠𝗨𝗧𝗛 𝗗𝗜𝗔 💦💦💦💦",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘 𝗔𝗔𝗔𝗚 𝗟𝗔𝗚𝗔𝗗𝗜𝗔 𝗠𝗘𝗥𝗔 𝗠𝗢𝗧𝗔 𝗟𝗨𝗡𝗗 𝗗𝗔𝗟𝗞𝗘 🔥🔥💦😆😆",
    "𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗢𝗗𝗨 𝗖𝗛𝗔𝗟 𝗡𝗜𝗞𝗔𝗟",
    "JARVIS OP",
    "𝗞𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗨 𝗧𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗔𝗕𝗕 𝗔𝗣𝗡𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗕𝗛𝗘𝗝 😆👻🤤",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢𝗧𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗣𝗨𝗥𝗔 𝗙𝗔𝗔𝗗 𝗗𝗜𝗔 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗔𝗕𝗕 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝 😆💦🤤",
    "𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗘𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗔 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗧𝗢 𝗠𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗕𝗔𝗡𝗚𝗔𝗬𝗜 𝗔𝗕𝗕 𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗢𝗗𝗧𝗔 𝗙𝗜𝗥𝗦𝗘 ♥️💦😆😆😆😆",
    "𝗛𝗔𝗥𝗜 𝗛𝗔𝗥𝗜 𝗚𝗛𝗔𝗔𝗦 𝗠𝗘 𝗝𝗛𝗢𝗣𝗗𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 🤣🤣💋💦",
    "𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗘 𝗕𝗔𝗔𝗣 𝗞𝗢 𝗕𝗛𝗘𝗝 𝗧𝗘𝗥𝗔 𝗕𝗔𝗦𝗞𝗔 𝗡𝗛𝗜 𝗛𝗘 𝗣𝗔𝗣𝗔 𝗦𝗘 𝗟𝗔𝗗𝗘𝗚𝗔 𝗧𝗨",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗕𝗢𝗠𝗕 𝗗𝗔𝗟𝗞𝗘 𝗨𝗗𝗔 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔́𝗔̀𝗞𝗘 𝗟𝗔𝗪𝗗𝗘",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗧𝗥𝗔𝗜𝗡 𝗠𝗘 𝗟𝗘𝗝𝗔𝗞𝗘 𝗧𝗢𝗣 𝗕𝗘𝗗 𝗣𝗘 𝗟𝗜𝗧𝗔𝗞𝗘 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 🤣🤣💋💋",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔𝗞𝗘 𝗡𝗨𝗗𝗘𝗦 𝗚𝗢𝗢𝗚𝗟𝗘 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗘 𝗟𝗔𝗘𝗪𝗗𝗘 👻🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗩𝗜𝗗𝗘𝗢 𝗕𝗔𝗡𝗔𝗞𝗘 𝗫𝗡𝗫𝗫.𝗖𝗢𝗠 𝗣𝗘 𝗡𝗘𝗘𝗟𝗔𝗠 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗞𝗨𝗧𝗧𝗘 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💦💋",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗢 𝗣𝗢𝗥𝗡𝗛𝗨𝗕.𝗖𝗢𝗠 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘 🤣💋💦",
    "𝗔𝗕𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗𝗨 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗘𝗞𝗢 𝗖𝗛𝗔𝗞𝗞𝗢 𝗦𝗘 𝗣𝗜𝗟𝗪𝗔𝗩𝗨𝗡𝗚𝗔 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 🤣🤣",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗙𝗔𝗔𝗗𝗞𝗘 𝗥𝗔𝗞𝗗𝗜𝗔 𝗠𝗔́𝗔̀𝗞𝗘 𝗟𝗢𝗗𝗘 𝗝𝗔𝗔 𝗔𝗕𝗕 𝗦𝗜𝗟𝗪𝗔𝗟𝗘 👄👄",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗠𝗘𝗥𝗔 𝗟𝗨𝗡𝗗 𝗞𝗔𝗔𝗟𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗟𝗘𝗧𝗜 𝗠𝗘𝗥𝗜 𝗟𝗨𝗡𝗗 𝗕𝗔𝗗𝗘 𝗠𝗔𝗦𝗧𝗜 𝗦𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗠𝗘𝗡𝗘 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗕𝗢𝗛𝗢𝗧 𝗦𝗔𝗦𝗧𝗘 𝗦𝗘",
    "𝗕𝗘𝗧𝗘 𝗧𝗨 𝗕𝗔𝗔𝗣 𝗦𝗘 𝗟𝗘𝗚𝗔 𝗣𝗔𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗞𝗔𝗥𝗞𝗘 𝗡𝗔𝗡𝗚𝗔 💦💋",
    "𝗛𝗔𝗛𝗔𝗛𝗔𝗛 𝗠𝗘𝗥𝗘 𝗕𝗘𝗧𝗘 𝗔𝗚𝗟𝗜 𝗕𝗔𝗔𝗥 𝗔𝗣𝗡𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗟𝗘𝗞𝗘 𝗔𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗧 𝗢𝗥 𝗠𝗘𝗥𝗘 𝗠𝗢𝗧𝗘 𝗟𝗨𝗡𝗗 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗥",
    "𝗖𝗛𝗔𝗟 𝗕𝗘𝗧𝗔 𝗧𝗨𝗝𝗛𝗘 𝗠𝗔́𝗔̀𝗙 𝗞𝗜𝗔 🤣 𝗔𝗕𝗕 𝗔𝗣𝗡𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝",
    "𝗦𝗛𝗔𝗥𝗔𝗠 𝗞𝗔𝗥 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗞𝗜𝗧𝗡𝗔 𝗚𝗔𝗔𝗟𝗜𝗔 𝗦𝗨𝗡𝗪𝗔𝗬𝗘𝗚𝗔 𝗔𝗣𝗡𝗜 𝗠𝗔́𝗔̀𝗔 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗘 𝗨𝗣𝗘𝗥",
    "𝗔𝗕𝗘 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗔𝗨𝗞𝗔𝗧 𝗡𝗛𝗜 𝗛𝗘𝗧𝗢 𝗔𝗣𝗡𝗜 𝗥Æ𝗡𝗗𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗟𝗘𝗞𝗘 𝗔𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗥 𝗛𝗔𝗛𝗔𝗛𝗔𝗛𝗔",
    "𝗞𝗜𝗗𝗭 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗧𝗘𝗥𝗥 𝗟𝗜𝗬𝗘 𝗕𝗛𝗔𝗜 𝗗𝗘𝗗𝗜𝗬𝗔",
    "𝗝𝗨𝗡𝗚𝗟𝗘 𝗠𝗘 𝗡𝗔𝗖𝗛𝗧𝗔 𝗛𝗘 𝗠𝗢𝗥𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗗𝗘𝗞𝗞𝗘 𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 🤣🤣💦💋",
    "𝗚𝗔𝗟𝗜 𝗚𝗔𝗟𝗜 𝗠𝗘 𝗥𝗘𝗛𝗧𝗔 𝗛𝗘 𝗦𝗔𝗡𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗢𝗥 𝗕𝗔𝗡𝗔 𝗗𝗜𝗔 𝗥𝗔𝗡𝗗 🤤🤣",
    "𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗠𝗨𝗝𝗛𝗞𝗢 𝗣𝗔𝗣𝗔 𝗞𝗬𝗢𝗨𝗡𝗞𝗜 𝗠𝗘𝗡𝗘 𝗕𝗔𝗡𝗔𝗗𝗜𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗣𝗥𝗘𝗚𝗡𝗘𝗡𝗧 🤣🤣",
    "𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗦𝗨𝗔𝗥 𝗞𝗔 𝗟𝗢𝗨𝗗𝗔 𝗢𝗥 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗠𝗘𝗥𝗔 𝗟𝗢𝗗𝗔",
    "𝗖𝗛𝗔𝗟 𝗖𝗛𝗔𝗟 𝗔𝗣𝗡𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗖𝗛𝗜𝗬𝗔 𝗗𝗜𝗞𝗔",
    "𝗛𝗔𝗛𝗔𝗛𝗔𝗛𝗔 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗜𝗔 𝗡𝗔𝗡𝗚𝗔 𝗞𝗔𝗥𝗞𝗘",
    "𝗧𝗘𝗥𝗜 𝗚𝗙 𝗛𝗘 𝗕𝗔𝗗𝗜 𝗦𝗘𝗫𝗬 𝗨𝗦𝗞𝗢 𝗣𝗜𝗟𝗔𝗞𝗘 𝗖𝗛𝗢𝗢𝗗𝗘𝗡𝗚𝗘 𝗣𝗘𝗣𝗦𝗜",
    "2 𝗥𝗨𝗣𝗔𝗬 𝗞𝗜 𝗣𝗘𝗣𝗦𝗜 𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗦𝗔𝗕𝗦𝗘 𝗦𝗘𝗫𝗬 💋💦",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗘𝗘𝗠𝗦 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔𝗩𝗨𝗡𝗚𝗔 𝗠𝗔𝗗𝗘𝗥𝗖𝗛𝗢𝗢𝗗 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💦🤣",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗠𝗨𝗧𝗛𝗞𝗘 𝗙𝗔𝗥𝗔𝗥 𝗛𝗢𝗝𝗔𝗩𝗨𝗡𝗚𝗔 𝗛𝗨𝗜 𝗛𝗨𝗜 𝗛𝗨𝗜",
    "𝗦𝗣𝗘𝗘𝗗 𝗟𝗔𝗔𝗔 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗖𝗛𝗢𝗗𝗨 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💋💦🤣",
    "𝗔𝗥𝗘 𝗥𝗘 𝗠𝗘𝗥𝗘 𝗕𝗘𝗧𝗘 𝗞𝗬𝗢𝗨𝗡 𝗦𝗣𝗘𝗘𝗗 𝗣𝗔𝗞𝗔𝗗 𝗡𝗔 𝗣𝗔𝗔𝗔 𝗥𝗔𝗛𝗔 𝗔𝗣𝗡𝗘 𝗕𝗔𝗔𝗣 𝗞𝗔 𝗛𝗔𝗛𝗔𝗛🤣🤣",
    "𝗦𝗨𝗡 𝗦𝗨𝗡 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗝𝗛𝗔𝗡𝗧𝗢 𝗞𝗘 𝗦𝗢𝗨𝗗𝗔𝗚𝗔𝗥 𝗔𝗣𝗡𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗡𝗨𝗗𝗘𝗦 𝗕𝗛𝗘𝗝",
    "𝗔𝗕𝗘 𝗦𝗨𝗡 𝗟𝗢𝗗𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗙𝗔𝗔𝗗 𝗗𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗞𝗛𝗨𝗟𝗘 𝗕𝗔𝗝𝗔𝗥 𝗠𝗘 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 🤣🤣💋",
    "𝗦𝗛𝗔𝗥𝗔𝗠 𝗔𝗔 𝗚𝗬𝗜 𝗛𝗔𝗜 𝗧𝗢 𝗡𝗔𝗭𝗥𝗘𝗡 𝗝𝗛𝗨𝗞𝗔 𝗟𝗜𝗝𝗜𝗬𝗘 𝗢𝗥 𝗔𝗚𝗔𝗥 𝗟𝗨𝗡𝗗 𝗠𝗘 𝗗𝗔𝗠 𝗡𝗛𝗜 𝗧𝗢 𝗦𝗛𝗜𝗟𝗔𝗝𝗘𝗘𝗧 𝗞𝗛𝗔 𝗟𝗜𝗝𝗜𝗬𝗘...🤣😂😂",
    
]
love_messages = [
        "Tᴇʀᴇ ɴᴀᴀʟᴏ ᴄʜᴀʟʟɪʏᴇ ʜᴀsᴇᴇɴ ᴋᴏʏɪ NA 😁😁",
    "Tᴀᴀʀᴇ ᴄʜᴀɴɴ ᴀᴍʙᴀʀ ᴢᴀᴍᴇᴇɴ ᴋᴏʏɪ ɴA",
    "Mᴀɪɴ Jᴀᴅᴏ Tᴇʀᴇ Mᴏᴅᴇ Uᴛᴛᴇ Sɪʀ Rᴀᴋʜᴇʏᴀ🧐🧐",
    "Eʜ Tᴏɴ Sᴀᴄʜɪ Sᴀᴍᴀ Vɪ Hᴀsᴇᴇɴ Kᴏɪ Nᴀ😖😖",
    "Sᴏʜɴɪʏᴀɴ Vɪ Lᴀɢɢᴀɴ Gɪʏᴀɴ Fᴇʀ Wᴀʟɪᴀɴ😍😍",
    "Gᴀʟᴀɴ Nᴀʟ Jᴀᴅᴏ Tᴀᴋʀᴀɪʏᴀɴ Wᴀʟɪʏᴀɴ🥰🥰",
    "Tᴀʀᴇ Dᴇᴋʜɪ Lᴀʙʜ Lᴀʙʜ Kɪᴠᴇɴ Hᴀʀᴅᴇ😁😁",
    "Tᴜ Bᴀʟᴀ Cʜ Lᴀᴋᴏɪʏᴀɴ Jᴀᴅᴏ Rᴀᴛᴀɴ Kᴀʟɪʏᴀɴ😒😒",
    "Mᴀɪɴ Sᴀʙ KᴜJ Hᴀʀ Tᴇʀᴇ Uᴛᴛᴏɴ Dᴇ’ᴜɴɢᴀ😌😌",
    "Sᴀʙ KᴜJ Wᴀʀ Tᴇʀᴇ Uᴛᴛᴏɴ Dᴇ’ᴜɴɢᴀ😉😉",
    "Aᴋʜɪʀ Cʜ Jᴀɴ Tᴀɪɴᴜ Dᴇ’ᴜɴ Aᴘɴɪ😎😎",
    "Cʜᴀʟᴀ Tᴀɪɴᴜ Bʜᴀᴠᴇɪɴ Pᴇʜʟɪ Wᴀʀ Dᴇ’ᴜɴɢᴀ😚😚",
    "Hᴀɴ Mᴀɪɴ Cʜᴇᴛɪ Cʜᴇᴛɪ Lᴀᴡᴀɴ😫😫",
    "Tᴇʀᴇ Nᴀʟ Lᴀɪɴɪ ᴀɴ😣😣",
    "Sᴀᴍᴀʏ Dᴀ Tᴀɴ Bʜᴏʀᴀ Vɪ Yᴀᴋᴇᴇɴ Kᴏɪ Nᴀ🥺🥺",
    "Tᴇʀᴇ Nᴀʟᴏ Jʜᴀʟɪʏᴇ Hᴀsᴇᴇɴ Kᴏɪ Nᴀ🥰🥰",
    "Tᴀʀᴇ Cʜᴀɴɴ Aᴍʙᴀʀ Zᴀᴍᴇᴇɴ Kᴏɪ Nᴀ😘😘",
    "Tᴜ Yᴀʀ Mᴇʀᴀ Tᴜ Hɪ Aᴇ Sᴀʜᴀʀᴀ AᴅɪʏE",
    "Mᴀɪɴ Pᴀɴɪ Tᴇʀᴀ Mᴇʀᴀ Tᴜ Kɪɴᴀʀᴀ Aᴅɪʏᴇ",
    "Pʜᴜʟ Bᴀɴ Jᴀɪ Mᴀɪɴ Kʜᴜsʜʙᴏᴏ Bᴀɴɴ Jᴜ",
    "Dᴇᴇᴠᴀɴ Bᴀɴɪ Mᴇʀᴀ Tᴇʀɪ Lᴀᴜ Bᴀɴ Jᴜ",
    "Hᴀʏᴇ UJᴀᴅɪʏᴀɴ Tʜᴀᴡᴀɴ Tᴇ Bᴀɴᴀᴛᴇ Bᴀɢ Nᴇ",
    "Tᴇʀɪʏᴀɴ Aɴᴋʜᴀɴ Nᴇ Kɪᴛᴛᴇ Jᴀᴅᴜ Yᴀᴅ Nᴇ",
    "Jᴀᴅᴏ Wᴀɴɢ Kᴏʟᴏɴ Pʜᴀᴅɪ Vɪ Nɪ KᴀssKᴇ",
    "Tᴏᴛᴛᴇ Sᴀᴍʙʜ Rᴀᴋʜᴇ Tᴜᴛᴛᴇ Hᴏʏᴇ Kᴀᴄʜ Dᴇ",
    "Hᴀɴ Kɪ Dɪʟ Yᴀᴅᴀɴ Rᴀᴋʜᴅᴀ Aᴇ, Sᴀᴍʙʜ Sᴀᴍʙʜ Kᴇ",
    "Hᴏʀ Dɪʟ SᴀJJɴᴀ Mᴀᴄʜɪɴᴇ Kᴏɪ Nᴀ",
    "Tᴇʀᴇ Nᴀʟᴏ Jʜᴀʟɪʏᴇ Hᴀsᴇᴇɴ Kᴏɪ Nᴀ",
    "Tᴀʀᴇ Cʜᴀɴɴ Aᴍʙᴀʀ Zᴀᴍᴇᴇɴ Kᴏɪ Nᴀ",
    "Mᴀɪɴ Jᴀᴅᴏ Tᴇʀᴇ Mᴏᴅᴇ Uᴛᴛᴇ Sɪʀ Rᴀᴋʜᴇʏᴀ",
    "Eʜ Tᴏɴ Sᴀᴄʜɪ Sᴀᴍᴀ Vɪ Hᴀsᴇᴇɴ Kᴏɪ Nᴀ",
    "Kɪɴᴇ Dɪɴ Hᴏɢʏᴇ Mᴇʀɪ Aᴋʜ Sᴏɪ Nᴀ",
    "Tᴇʀᴇ Tᴏɴ Bᴀɢᴀɪʀ Mᴇʀᴀ Aɪᴛʜᴇ Kᴏɪ Nᴀ",
    "Tᴜ Bʜᴜᴋʜ Vɪ Aᴇ Tᴜ Hɪ Aᴇ Gᴜᴢᴀʀᴀ Aᴅɪʏᴇ",
    "Mᴀɴɴᴜ Sᴀʙ Kᴀʀɪ Tᴜ Isʜᴀʀᴀ Aᴅɪʏᴇ",
    "Hᴏ Kʜᴀᴜʀᴇ Kɪɴɴɪ Wᴀʀ Sᴇᴇɴᴇ Vɪᴄʜ Kʜᴜʙɪʏᴀɴ",
    "Sᴜʀᴍᴇ Dᴇ Vɪᴄʜ Dᴏᴠᴇɪɴ Aɴᴋʜᴀɴ Dᴜʙʙɪʏᴀɴ",
    "Kɪɴɪ Sᴏʜɴɪ Lᴀɢɢᴇ Jᴀᴅᴏɴ Cʜᴜᴘ Kᴀʀ Jᴇ",
    "Jᴀɴᴅɪ Jᴀɴᴅɪ Sʜᴀᴍᴀɴ Nᴜ Vɪ Dʜᴜᴘ Kᴀʀ Jᴇ",
    "Hᴀʏᴇ Mᴀɪɴ Pᴀᴜɴ Fᴀʀᴍᴀɪsʜɪ Rᴀɴɢ Tᴇʀᴇ Sᴏʜɴɪʏᴇ",
    "UɴJ Bᴀʜᴏᴛᴀɴ Gɪғᴛʏ Sʜᴀᴜᴋᴇᴇɴ Kᴏɪ Nᴀ",
    "Tᴀʀᴇ Cʜᴀɴɴ Aᴍʙᴀʀ Zᴀᴍᴇᴇɴ Kᴏɪ Nᴀ🥰🥰",
    "Tᴇʀᴇ Nᴀʟᴏ Jʜᴀʟɪʏᴇ Hᴀsᴇᴇɴ Kᴏɪ Nᴀ😍😍",
    "Mᴀɪɴ Jᴀᴅᴏ Tᴇʀᴇ Mᴏᴅᴇ Uᴛᴛᴇ Sɪʀ Rᴀᴋʜᴇʏᴀ😁😁",
    "Eʜ Tᴏɴ Sᴀᴄʜɪ Sᴀᴍᴀ Vɪ Hᴀsᴇᴇɴ Kᴏɪ Nᴀ😒😒",
    "Kᴀɴɴᴀ Wɪᴄʜ Jʜᴜᴍᴋᴀ👀👀",
    "Aᴋʜᴀɴ Wɪᴄʜ Sᴜʀᴍᴀ🙈🙈",
    "Hᴏ Jᴀɪsᴇ Sᴛʀᴀᴡʙᴇʀʀʏ Cᴀɴᴅʏ😋😋",
    "Nᴀᴋᴋ Uᴛᴛᴇ Kᴏᴋᴀ🤨🤨",
    "Jᴇᴇɴᴀ Kᴀʀᴇ Aᴜᴋʜᴀ🤭🤭",
    "Hᴀʏᴇ Mᴇʀɪ Jᴀᴀɴ Kᴀᴅᴅ Lᴀɪɴᴅɪ😌😌",
    "Tᴇʀᴇ Nᴀᴋʜʀᴇ Hᴀʏᴇ Tᴀᴜʙᴀ Sᴀɴᴜ Mᴀᴀʀᴅᴇ🤫🤫",
    "Hᴏ Gᴀʏᴀ Hᴀɪ Mᴇʀᴀ Bᴀʙʏ Bᴜʀᴀ HᴀᴀL😊😊",
    "Sᴀᴄʜɪ Lᴜᴛ Gᴀʏᴇ Hᴜᴍ Tᴇʀᴇ Is Pʏᴀʀ Mᴇɪɴ😏😏",
    "Jᴇᴇɴɪ Zɪɴᴅᴀɢɪ Hᴀɪ Bᴀs Tᴇʀᴇ Nᴀᴀʟ😚😚",
    "I Lᴏᴠᴇ YᴏU SO MUCH 😍😍",
    "ᴄᴀᴜsᴇ I Lᴏᴠᴇ Yᴏᴜ 😘😘",
    "Sᴀᴘɴᴏ Mᴇɪɴ Mᴇʀᴇ AᴀʏI😝😝",
    "Bᴀʙʏ! Lᴀɢᴇ Sᴏʜɴᴀ Kɪᴛɴᴀ PʏᴀʀA😚😚",
    "Sᴀᴘɴᴏ Mᴇɪɴ Mᴇʀᴇ Aᴀʏɪ😝😝",
    "Uғғ Oʜ Pʜɪʀ Nᴇᴇɴᴅᴇɪɴ Hɪ Cʜᴜʀᴀʏɪ😜😜",
    "Oʜ Nᴏ! Tᴇʀᴀ Hᴜsᴀɴ Nᴀᴢᴀʀᴀ🥰🥰",
    "Tᴀɪɴᴜ Dɪᴀᴍᴏɴᴅ Mᴜɴᴅʀɪ Pᴇʜɴᴀᴡᴀ😎😎",
    "Nᴀᴀʟᴇ Dᴜɴɪʏᴀ Sᴀʀɪ Gʜᴜᴍᴀᴡᴀ🙈🙈",
    "Cʜʜᴏᴛɪ-Cʜʜᴏᴛɪ Gᴀʟʟᴀɴ Uᴛᴛᴇ Mᴀɪɴ Hᴀsᴀᴠᴀᴀɴ💙💙",
    "Yᴀᴀʀᴀ Kᴀᴅᴇ Vɪ Nᴀ Tᴀɪɴᴜ Mᴀɪɴ Rᴜʟᴀᴡᴀᴀɴ🙊🙊",
    "ᴄᴀᴜsᴇ I Lᴏᴠᴇ Yᴏᴜ  🙈🙈",
    "I Lᴏᴠᴇ Yᴏᴜ ❤️❤️",
    "ᴄᴀᴜsᴇ I Lᴏᴠᴇ Yᴏᴜ🙈🙈",
    "Yᴀᴀʀɪ Lᴀᴀᴡᴀɴ Sᴀᴄʜɪ YᴀᴀʀI💫💫",
    "Tᴜ Jᴀᴀɴ Tᴏɴ Vɪ Pʏᴀʀɪ😁😁",
    "Wɪʟʟ Lᴏᴠᴇ Yᴏᴜ Tᴏ Tʜᴇ Mᴏᴏɴ Aɴᴅ Bᴀᴄᴋ😆😆",
    "Hᴏɢɪ Sᴀᴢᴀ Nᴀ Kᴏʏɪ Hᴏɢɪ😙😙",
    "Cʜᴀʜᴇ Kᴀʀᴜɴ Cʜᴏʀɪ Cʜᴀᴀɴᴅ Tᴀᴀʀᴇ😉😉",
    "Iᴍᴍᴀ Gɪᴠᴇ Yᴏᴜ Tʜᴇᴍ😅😅",
    "Yᴀᴀʀɪ Lᴀᴀᴠᴀɴ Sᴀᴄʜɪ YᴀᴀʀI😘😘",
    "Tᴜ Jᴀᴀɴ Tᴏɴ Vɪ PʏᴀʀI😆😆",
    "Wɪʟʟ Lᴏᴠᴇ Yᴏᴜ Tᴏ Tʜᴇ Mᴏᴏɴ Aɴᴅ Bᴀᴄᴋ💕💕",
    "Hᴏɢᴇᴇ Sᴀᴢᴀᴀ Nᴀ Kᴏʏɪ Hᴏɢɪ💓💓",
    "Cʜᴀʜᴇ Kᴀʀᴜɴ Cʜᴏʀɪ Cʜᴀᴀɴᴅ Tᴀᴀʀᴇ🥺🥺",
    "Iᴍᴍᴀ Gɪᴠᴇ Yᴏᴜ Tʜᴇᴍ🥵🥵",
    "Pᴜʀɪ Kᴀʀᴜɴɢᴀ Mᴀɪɴ Tᴇʀɪ Sᴀʀɪ Kʜᴀʜɪsʜᴇɪɴ😁😁",
    "Tᴇʀᴀ Rᴀᴋʜᴀɴɢᴀ Mᴀɪɴ RᴀJJ Kᴇ Kʜᴀʏᴀʟ😘😘",
    "Kɪᴛɴɪ Kʜᴏᴏʙɪʏᴀɴ Hᴀɪ Tᴇʀᴇ Is Yᴀᴀʀ Mᴇɪɴ🥰🥰",
    "AᴀJᴀ Bᴀʜᴏɴ Mᴇɪɴ Tᴜ Bᴀʜᴇɪɴ Bᴀs Dᴀᴀʟ😂😂",
    "Aᴜʀ Hᴏᴛᴀ Nᴀʜɪ Aʙ Iɴᴛᴇᴢᴀʀ🤩🤩",
    "Aᴜʀ Hᴏᴛᴀ Nᴀʜᴇᴇ Aʙ Iɴᴛᴇᴢᴀᴀʀ😘😘",
    "ᴄᴀᴜsᴇ I Lᴏᴠᴇ Yᴏᴜ 😍😍",
    "I Lᴏᴠᴇ YᴏU 😙😙",
    "ᴄᴀᴜsᴇ I Lᴏᴠᴇ Yᴏᴜ",
    "I Lᴏᴠᴇ YᴏU SOOOOOOOOOOOOOOOOOO MUCHHHHHHHHHHHHHHHHHHHHH 😘😘",
    "WILL U BE MINE FOREVER??🤔🤔",
    "Jᴇ ᴛᴜ ᴀᴋʜ ᴛᴇ ᴍᴀɪɴ ᴀᴀɴ ᴋᴀᴀJᴀʟ ᴠᴇ😌😌",
    "Tᴜ ʙᴀᴀʀɪsʜ ᴛᴇ ᴍᴀɪɴ ʙᴀᴀᴅᴀʟ ᴠᴇ🤫🤫",
    "Tᴜ ᴅᴇᴇᴡᴀɴᴀ ᴍᴀɪɴ ᴀᴀɴ ᴘᴀᴀɢᴀʟ ᴠᴇ🤪🤪",
    "Sᴏʜɴᴇʏᴀ sᴏʜɴᴇʏᴀ☺️☺️",
    "Jᴇ ᴛᴜ ᴄʜᴀɴɴ ᴛᴇ ᴍᴀɪɴ ᴀᴀɴ ᴛᴀᴀʀᴀ ᴠᴇ🤗🤗",
    "Mᴀɪɴ ʟᴇʜᴀʀ ᴛᴇ ᴛᴜ ᴋɪɴᴀʀᴀ ᴠᴇ😶😶",
    "Mᴀɪɴ ᴀᴀᴅʜᴀ ᴛᴇ ᴛᴜ sᴀᴀʀᴀ ᴠᴇ🤗🤗",
    "Sᴏʜɴᴇʏᴀ sᴏʜɴᴇʏᴀ😗😗",
    "Tᴜ Jᴀʜᴀɴ ʜᴀɪ ᴍᴀɪɴ ᴡᴀʜᴀɴ😘😘",
    "Tᴇʀᴇ ʙɪɴ ᴍᴀɪɴ ʜᴏᴏɴ ʜɪ ᴋʏᴀ🥲🥲",
    "Tᴇʀᴇ ʙɪɴ ᴄʜᴇʜʀᴇ sᴇ ᴍᴇʀᴇ🤔🤔",
    "Uᴅᴅ Jᴀᴀʏᴇ ʀᴀɴɢ ᴠᴇ😅😅",
    "TᴜJʜᴋᴏ ᴘᴀᴀɴᴇ ᴋᴇ ʟɪʏᴇ ʜᴜM😁😁",
    "Rᴏᴢ ᴍᴀɴɢᴇɪɴ ᴍᴀɴɴᴀᴛ ᴠᴇ🙈🙈",
    "Dᴜɴɪʏᴀ ᴛᴏ ᴋʏᴀ ᴄʜᴇᴇᴢ ʜᴀɪ ʏᴀᴀʀᴀ🙉🙉",
]
gali_messages = [
    " 𝐎𝐲𝐲 𝐭𝐞𝐫𝐞 𝐛𝐚𝐥𝐞 𝐤𝐨 𝐣𝐚𝐤𝐚𝐫 𝐛𝐚𝐭𝐚𝐭𝐚 𝐡𝐮 𝐭𝐮 𝐲𝐡𝐚 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐤𝐚𝐫 𝐫𝐡𝐢 𝐡𝐚𝐢🥱 ",
           " 𝐀𝐩𝐤𝐢 𝐞𝐤 𝐩𝐢𝐜 𝐦𝐢𝐥𝐞𝐠𝐢 𝐤𝐲𝐚 𝐢𝐦𝐚𝐠𝐢𝐧𝐞 𝐤𝐚𝐫 𝐤𝐞 𝐦*𝐭𝐡 𝐤𝐚𝐫𝐧𝐚 𝐡𝐢 ",
           " 𝐕𝐜 𝐂𝐡𝐚𝐥𝐨 𝐑𝐨𝐦𝐚𝐧𝐭𝐢𝐜 𝐁𝐚𝐭𝐞𝐧 𝐊𝐚𝐫𝐭𝐞 𝐇𝐚𝐢𝐧 𝐊𝐮𝐜𝐡 𝐊𝐮𝐜𝐡😃 ",
           " 𝐓𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐭𝐮𝐦𝐡𝐚𝐫𝐚 𝐤𝐡𝐚𝐝𝐚 𝐡𝐨𝐭𝐚 𝐡𝐚𝐢 𝐤𝐲𝐚 😁🥲 ",
           " 𝐔𝐟𝐟 𝐊𝐲𝐚 𝐦𝐚𝐚𝐥 𝐡𝐚𝐢 𝐲𝐚𝐚𝐫 😁😂🥺 ",
           " 𝐏𝐭𝐚 𝐇𝐚𝐢 𝐁𝐨𝐡𝐨𝐭 𝐌𝐢𝐬𝐬 𝐊𝐚𝐫 𝐑𝐡a 𝐓𝐡a 𝐀𝐚𝐩𝐤𝐨 𝐛𝐚𝐭𝐡𝐫𝐨𝐨𝐦 𝐦𝐞 🤭 ",
           " 𝐎𝐲𝐞 𝐃𝐌 𝐊𝐚𝐫𝐨 𝐀𝐩𝐤𝐚 𝐦𝐨𝐨𝐝 𝐛𝐧𝐚 𝐝𝐞𝐭𝐢 𝐡𝐮 😅😅 ",
           " 𝐌𝐞𝐫𝐢 𝐁𝐡𝐢 𝐒𝐞𝐭𝐭𝐢𝐧𝐠 𝐊𝐚𝐫𝐛𝐚 𝐃𝐨𝐠𝐞.𝐇𝐢𝐥𝐥𝐚 𝐇𝐢𝐥𝐥𝐚 𝐤𝐞 𝐭𝐡𝐚𝐤 𝐠𝐲𝐚 𝐡𝐮 ??🙂 ",
           " 𝐎𝐲𝐲 𝐭𝐞𝐫𝐞 𝐛𝐚𝐥𝐞 𝐤𝐨 𝐣𝐚𝐤𝐚𝐫 𝐛𝐚𝐭𝐚𝐭𝐚 𝐡𝐮 𝐭𝐮 𝐲𝐡𝐚 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐤𝐚𝐫 𝐫𝐡𝐢 𝐡𝐚𝐢🥲 ",
           " 𝐤𝐚 𝐡𝐨 𝐤𝐚𝐫𝐞𝐣𝐚 1 𝐜𝐡𝐮𝐦𝐦𝐚 𝐧𝐚 𝐝𝐞𝐛𝐮 😅😋 ",
           " 𝐎𝐲𝐲 𝐌𝐞𝐫𝐞 𝐊𝐨 𝐀𝐩𝐧𝐞 𝐛𝐞𝐝𝐫𝐨𝐨𝐦 𝐦𝐞 𝐤𝐢𝐝𝐧𝐞𝐩 𝐤𝐚𝐫 𝐥o😅😅  ",
           " 𝐀𝐚𝐩𝐤𝐢 𝐏𝐚𝐫𝐭𝐧𝐞𝐫 𝐀𝐚𝐩𝐤𝐨 𝐃𝐡𝐮𝐧𝐝 𝐑𝐡𝐞 𝐇𝐚𝐢𝐧 𝐉𝐥𝐝𝐢 𝐎𝐧𝐥𝐢𝐧𝐞 𝐀𝐲𝐢𝐚𝐞😅😅 ",
           " 𝐇𝐚𝐦 𝐃𝐨𝐬𝐭 𝐁𝐚𝐧 𝐒𝐚𝐤𝐭𝐞 𝐇𝐚𝐢...?🥰 𝐌𝐚𝐬𝐭𝐞𝐫𝐛𝐚𝐭𝐢𝐧𝐠 𝐤𝐚𝐫𝐧𝐞 𝐦𝐞 𝐡𝐞𝐥𝐩 𝐡𝐨 𝐣𝐚𝐲𝐞𝐠𝐢 𝐦𝐞𝐫𝐢 😁🤔 ",
           " 𝐒𝐨𝐧𝐞 𝐂𝐡𝐚𝐥 𝐆𝐲𝐞 𝐊𝐲𝐚 𝐉𝐀𝐍𝐄𝐌𝐀𝐍 🙄🙄 ",
           " 𝐇𝐚𝐦 𝐃𝐨𝐬𝐭 𝐁𝐚𝐧 𝐒𝐚𝐤𝐭𝐞 𝐇𝐚𝐢...?🥰 𝐌𝐚𝐬𝐭𝐞𝐫𝐛𝐚𝐭𝐢𝐧𝐠 𝐤𝐚𝐫𝐧𝐞 𝐦𝐞 𝐡𝐞𝐥𝐩 𝐡𝐨 𝐣𝐚𝐲𝐞𝐠𝐢 𝐦𝐞𝐫𝐢 😁 😁😕 ",
           " 𝐲𝐨𝐮𝐫 𝐟𝐚𝐯𝐨𝐮𝐫𝐢𝐭𝐞 𝐚𝐜𝐭𝐫𝐞𝐬𝐬 (𝐒𝐔𝐍𝐍𝐘 𝐋𝐄𝐎𝐍𝐄, 𝐨𝐫 𝐌𝐈𝐘𝐀 𝐊𝐇𝐀𝐋𝐈𝐅𝐀)🙃 ",
           " 𝐎𝐲𝐲 𝐏𝐫𝐢𝐲𝐚 𝐁𝐡𝐚𝐛𝐡𝐢 𝐤𝐚 𝐤𝐲𝐚 𝐡𝐚𝐢 😁😁😛 ",
           " 𝐇𝐞𝐥𝐥𝐨 𝐁𝐚𝐛𝐲 𝐊𝐤𝐫𝐡..?🤔 ",
           " 𝐎𝐲𝐲 𝐬𝐮𝐧𝐨 𝐀𝐩 𝐑𝐨𝐣 𝐡𝐢𝐥𝐚𝐭𝐞 𝐡𝐨 𝐤𝐲𝐚 𝐩𝐚𝐭𝐥𝐞 𝐡𝐨 𝐠𝐲𝐞 𝐡𝐨 😅 ",
           " 𝐂𝐡𝐥𝐨 𝐇𝐚𝐦 𝐝𝐨𝐧𝐨 𝐫𝐚𝐭 𝐛𝐚𝐥𝐚.𝐠𝐚𝐧𝐞 𝐤𝐡𝐚𝐭𝐞 𝐡𝐚𝐢 😁.🤗 ",
           " 𝐂𝐡𝐚𝐥𝐨 𝐡𝐚𝐦 𝐝𝐨𝐧𝐨 𝐫𝐨𝐦𝐚𝐧𝐭𝐢𝐜 𝐛𝐚𝐭𝐞 𝐤𝐚𝐫𝐭𝐞 𝐡𝐚𝐢 😇 ",
           " 𝐨𝐨𝐲 𝐦𝐞𝐫𝐢 𝐡𝐞𝐥𝐩 𝐤𝐚𝐫𝐨𝐠𝐞 𝐦𝐚𝐬𝐭𝐞𝐫𝐛𝐚𝐭𝐞 𝐤𝐚𝐫𝐧𝐞 𝐦𝐞 😁🤭 ",
           " 𝐎𝐲𝐲 𝐭𝐮 𝐢𝐭𝐧𝐢 𝐡𝐨𝐭 𝐤𝐲𝐮 𝐡𝐚𝐢 𝐝𝐞𝐤𝐡𝐭𝐞 𝐡𝐢 𝐦𝐚𝐧 𝐤𝐚𝐫𝐭𝐚 𝐡𝐚𝐢 𝐡𝐢𝐥𝐚 𝐥𝐮 😁😀🥺🥺 ",
           " 𝐎𝐲𝐞 𝐏𝐚𝐠𝐚𝐥 𝐚𝐩𝐤𝐢 𝐚𝐠𝐞 𝐤𝐲𝐚 𝐡𝐚𝐢 𝐡𝐨𝐭 𝐥𝐠𝐭𝐞 𝐡𝐨 𝐚𝐩😶 ",
           " 𝐀𝐚𝐣 𝐇𝐨𝐥𝐢𝐝𝐚𝐲 𝐇𝐚𝐢 𝐊𝐲𝐚 𝐒𝐜𝐡𝐨𝐨𝐥 𝐌𝐞..??🤔 ",
           " 𝐤𝐚 𝐡𝐨 𝐤𝐚𝐫𝐞𝐣𝐚 1 𝐜𝐡𝐮𝐦𝐦𝐚 𝐧𝐚 𝐝𝐞𝐛𝐮 😅😜 ",
           " 𝐌𝐞𝐫𝐢 𝐁𝐡𝐢 𝐒𝐞𝐭𝐭𝐢𝐧𝐠 𝐊𝐚𝐫𝐛𝐚 𝐃𝐨𝐠𝐞.𝐇𝐢𝐥𝐥𝐚 𝐇𝐢𝐥𝐥𝐚 𝐤𝐞 𝐭𝐡𝐚𝐤 𝐠𝐲𝐚 𝐡𝐮 🙂🙂 ",
           " 𝐚𝐩𝐤𝐢 𝐚𝐠𝐞 𝐤𝐲𝐚 𝐡𝐚𝐢 𝐡𝐨𝐭 𝐡𝐨 𝐚𝐩 𝐝𝐞𝐤𝐡𝐭𝐞 𝐡𝐢 𝐦𝐚𝐧 𝐤𝐚𝐫𝐭𝐚 𝐡𝐢𝐥𝐚𝐭𝐞 𝐫𝐡𝐮😁😪 ",
           " 𝐍𝐢𝐜𝐞 𝐓𝐨 𝐌𝐞𝐞𝐭 𝐔𝐡 𝐉𝐀𝐍𝐄𝐌𝐀𝐍☺ ",
           " 𝐇𝐞𝐥𝐥𝐨 𝐀𝐩𝐤𝐚 𝐛𝐫𝐞𝐚𝐤 𝐮𝐩 𝐤𝐚𝐫𝐛𝐚 𝐝𝐞𝐭𝐚 𝐡𝐮 𝐚𝐩 𝐦𝐞𝐫𝐞 𝐬𝐞 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐤𝐚𝐫𝐥𝐨 😀😁🙊 ",
           " 𝐎𝐲𝐲 𝐭𝐞𝐫𝐞 𝐛𝐚𝐥𝐞 𝐤𝐨 𝐣𝐚𝐤𝐚𝐫 𝐛𝐚𝐭𝐚𝐭𝐚 𝐡𝐮 𝐭𝐮 𝐲𝐡𝐚 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐤𝐚𝐫 𝐫𝐡𝐢 𝐡𝐚𝐢😺 ",
           " 𝐎𝐲𝐲 𝐬𝐮𝐧𝐨 𝐀𝐩 𝐑𝐨𝐣 𝐡𝐢𝐥𝐚𝐭𝐞 𝐡𝐨 𝐤𝐲𝐚 𝐩𝐚𝐭𝐥𝐞 𝐡𝐨 𝐠𝐲𝐞 𝐡𝐨🥲 ",
           " 𝐎𝐲𝐲 𝐭𝐞𝐫𝐞 𝐛𝐚𝐥𝐞 𝐤𝐨 𝐣𝐚𝐤𝐚𝐫 𝐛𝐚𝐭𝐚𝐭𝐚 𝐡𝐮 𝐭𝐮 𝐲𝐡𝐚 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐤𝐚𝐫 𝐫𝐡𝐢 𝐡𝐚𝐢😅 ",
           " 𝐀𝐩𝐤𝐢 𝐞𝐤 𝐩𝐢𝐜 𝐦𝐢𝐥𝐞𝐠𝐢 𝐤𝐲𝐚 𝐢𝐦𝐚𝐠𝐢𝐧𝐞 𝐤𝐚𝐫 𝐤𝐞 𝐦*𝐭𝐡 𝐤𝐚𝐫𝐧𝐚 𝐡𝐢😅 ",
           " 𝐓𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐭𝐮𝐦𝐡𝐚𝐫𝐚 𝐤𝐡𝐚𝐝𝐚 𝐡𝐨𝐭𝐚 𝐡𝐚𝐢 𝐤𝐲𝐚 😁😆😆😆 ",
           " 𝐎𝐫 𝐁𝐚𝐭𝐚𝐨 𝐁𝐡𝐚𝐛𝐡𝐢 𝐊𝐚𝐢𝐬𝐢 𝐇𝐚𝐢😉 ",
           " 𝐀𝐚𝐣 𝐓𝐮𝐦 𝐟𝐢𝐧𝐠𝐞𝐫 𝐬𝐞 𝐡𝐢 𝐤𝐚𝐚𝐦 𝐜𝐡𝐚𝐥𝐚𝐨. 𝐆𝐡𝐚𝐫 𝐦𝐞 𝐛𝐚𝐢𝐠𝐚𝐧 𝐨𝐫 𝐦𝐮𝐤𝐢 𝐤𝐡𝐚𝐭𝐚𝐦 𝐡𝐨 𝐠𝐲𝐞 𝐡𝐚𝐢 🙈🙈🙈 ",
           " 𝐎𝐲𝐲 𝐏𝐫𝐢𝐲𝐚 𝐁𝐡𝐚𝐛𝐡𝐢 𝐤𝐚 𝐤𝐲𝐚 𝐡𝐚𝐢 𝐡𝐚𝐢 😁😁👀 ",
           " 𝐲𝐨𝐮𝐫 𝐟𝐚𝐯𝐨𝐮𝐫𝐢𝐭𝐞 𝐚𝐜𝐭𝐫𝐞𝐬𝐬 (𝐒𝐔𝐍𝐍𝐘 𝐋𝐄𝐎𝐍𝐄, 𝐨𝐫 𝐌𝐈𝐘𝐀 𝐊𝐇𝐀𝐋𝐈𝐅𝐀)😹 ",
           " 𝐨 𝐡𝐞𝐥𝐥𝐨 𝐚𝐩𝐤𝐢 𝐚𝐠𝐞 𝐤𝐲𝐚 𝐡𝐚𝐢 𝐡𝐨𝐭 𝐥𝐠𝐭𝐞 𝐡𝐨 𝐚𝐩😻 ",
           " 𝐓𝐮𝐦 𝐫𝐨𝐣 𝐡𝐢𝐥𝐚𝐭𝐞 𝐡𝐨 𝐤𝐲𝐚 , 𝐁𝐡𝐮𝐭 𝐩𝐚𝐭𝐤𝐞 𝐡𝐢 𝐠𝐲𝐞 𝐡𝐨 💕😴🙃 ",
           " 𝐌𝐞𝐫𝐢 𝐁𝐡𝐢 𝐒𝐞𝐭𝐭𝐢𝐧𝐠 𝐊𝐚𝐫𝐛𝐚 𝐃𝐨𝐠𝐞.𝐇𝐢𝐥𝐥𝐚 𝐇𝐢𝐥𝐥𝐚 𝐤𝐞 𝐭𝐡𝐚𝐤 𝐠𝐲𝐚 𝐡𝐮 .??😕 ",
           " 𝐲𝐨𝐮𝐫 𝐟𝐚𝐯𝐨𝐮𝐫𝐢𝐭𝐞 𝐚𝐜𝐭𝐫𝐞𝐬𝐬 (𝐒𝐔𝐍𝐍𝐘 𝐋𝐄𝐎𝐍𝐄, 𝐨𝐫 𝐌𝐈𝐘𝐀 𝐊𝐇𝐀𝐋𝐈𝐅𝐀)🙃 ",
           " 𝐁𝐡𝐚𝐛𝐡𝐢 𝐣𝐢 𝐤𝐨 𝐤𝐡𝐮𝐬𝐡 𝐫𝐤𝐡𝐚 𝐤𝐚𝐫𝐨 𝐭𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐰𝐚𝐫𝐧𝐚 𝐤𝐢𝐬𝐢 𝐨𝐫 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐛𝐡𝐚𝐠 𝐣𝐚𝐲𝐞𝐠𝐢 😅😀😀?🙃 ",
           " 𝐉𝐡𝐚𝐭𝐞 𝐧𝐚 𝐜𝐡*𝐜*𝐈 𝐨𝐫 𝐛𝐚𝐭𝐞 𝐮𝐜𝐡𝐢 𝐮𝐜𝐡𝐢 😴😴😅 ",
           " 𝐌𝐞𝐫𝐢 𝐁𝐡𝐢 𝐒𝐞𝐭𝐭𝐢𝐧𝐠 𝐊𝐚𝐫𝐛𝐚 𝐃𝐨𝐠𝐞.𝐇𝐢𝐥𝐥𝐚 𝐇𝐢𝐥𝐥𝐚 𝐤𝐞 𝐭𝐡𝐚𝐤 𝐠𝐲𝐚 𝐡𝐮 .??🙂🧐 ",
           " 𝐌𝐞𝐫𝐚 𝐄𝐤 𝐊𝐚𝐚𝐦 𝐊𝐚𝐫 𝐃𝐨𝐠𝐞.𝐏𝐥𝐳 𝐦𝐮𝐭𝐡 𝐦𝐚𝐫 𝐝𝐨😁😁.? ",
           " 𝐁𝐡𝐚𝐛𝐡𝐢 𝐣𝐢 𝐤𝐨 𝐤𝐡𝐮𝐬𝐡 𝐫𝐤𝐡𝐚 𝐤𝐚𝐫𝐨 𝐭𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐰𝐚𝐫𝐧𝐚 𝐤𝐢𝐬𝐢 𝐨𝐫 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐛𝐡𝐚𝐠 𝐣𝐚𝐲𝐞𝐠𝐢 😅😀😀😠 ",
           " 𝐚𝐩𝐤𝐢 𝐚𝐠𝐞 𝐤𝐲𝐚 𝐡𝐚𝐢 𝐡𝐨𝐭 𝐡𝐨 𝐚𝐩 𝐝𝐞𝐤𝐡𝐭𝐞 𝐡𝐢 𝐦𝐚𝐧 𝐤𝐚𝐫𝐭𝐚 𝐡𝐢𝐥𝐚𝐭𝐞 𝐫𝐡𝐮😁❤ ",
           " 𝐎𝐲𝐲 𝐬𝐮𝐧𝐨 𝐀𝐩 𝐑𝐨𝐣 𝐡𝐢𝐥𝐚𝐭𝐞 𝐡𝐨 𝐤𝐲𝐚 𝐩𝐚𝐭𝐥𝐞 𝐡𝐨 𝐠𝐲𝐞 𝐡𝐨👱 ",
           " 𝐁𝐨𝐡𝐨𝐭 𝐘𝐚𝐚𝐝 𝐀𝐚 𝐑𝐡𝐢 𝐇𝐚𝐢 𝐁𝐡𝐚𝐛𝐡𝐢 𝐣𝐢 𝐤𝐚𝐢𝐬𝐢 𝐡𝐚𝐢🤧❣️ ",
           " 𝐎𝐲𝐲 𝐬𝐮𝐧𝐨 𝐀𝐩 𝐑𝐨𝐣 𝐡𝐢𝐥𝐚𝐭𝐞 𝐡𝐨 𝐤𝐲𝐚 𝐩𝐚𝐭𝐥𝐞 𝐡𝐨 𝐠𝐲𝐞 𝐡𝐨😏😏 ",
           " 𝐀𝐩𝐤𝐢 𝐞𝐤 𝐩𝐢𝐜 𝐦𝐢𝐥𝐞𝐠𝐢 𝐤𝐲𝐚 𝐢𝐦𝐚𝐠𝐢𝐧𝐞 𝐤𝐚𝐫 𝐤𝐞 𝐦*𝐭𝐡 𝐤𝐚𝐫𝐧𝐚 𝐡𝐢🤐 ",
           " 𝐁𝐡𝐚𝐛𝐡𝐢 𝐣𝐢 𝐤𝐨 𝐤𝐡𝐮𝐬𝐡 𝐫𝐤𝐡𝐚 𝐤𝐚𝐫𝐨 𝐭𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐰𝐚𝐫𝐧𝐚 𝐤𝐢𝐬𝐢 𝐨𝐫 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐛𝐡𝐚𝐠 𝐣𝐚𝐲𝐞𝐠𝐢 😅😀😀😒 ",
           " 𝐁𝐡𝐚𝐛𝐡𝐢 𝐣𝐢 𝐤𝐨 𝐤𝐡𝐮𝐬𝐡 𝐫𝐤𝐡𝐚 𝐤𝐚𝐫𝐨 𝐭𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐰𝐚𝐫𝐧𝐚 𝐤𝐢𝐬𝐢 𝐨𝐫 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐛𝐡𝐚𝐠 𝐣𝐚𝐲𝐞𝐠𝐢 😅😮😮 "
           " 𝐉𝐡𝐚𝐭𝐞 𝐧𝐚 𝐜𝐡*𝐜*𝐈 𝐨𝐫 𝐛𝐚𝐭𝐞 𝐮𝐜𝐡𝐢 𝐮𝐜𝐡𝐢 😴😴😅👀 ", 
           " 𝐀𝐩𝐤𝐢 𝐞𝐤 𝐩𝐢𝐜 𝐦𝐢𝐥𝐞𝐠𝐢 𝐤𝐲𝐚 𝐢𝐦𝐚𝐠𝐢𝐧𝐞 𝐤𝐚𝐫 𝐤𝐞 𝐦*𝐭𝐡 M𝐚𝐫𝐧𝐚 𝐡ai 😅😅 ",
           " 𝐁𝐡𝐚𝐛𝐡𝐢 𝐣𝐢 𝐤𝐨 𝐤𝐡𝐮𝐬𝐡 𝐫𝐤𝐡𝐚 𝐤𝐚𝐫𝐨 𝐭𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐰𝐚𝐫𝐧𝐚 𝐤𝐢𝐬𝐢 𝐨𝐫 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐛𝐡𝐚𝐠 𝐣𝐚𝐲𝐞𝐠𝐢 😅🥺🥺 ",
           " 𝐎𝐲𝐲 𝐬𝐮𝐧𝐨 𝐀𝐩 𝐑𝐨𝐣 𝐡𝐢𝐥𝐚𝐭𝐞 𝐡𝐨 𝐤𝐲𝐚 𝐩𝐚𝐭𝐥𝐞 𝐡𝐨 𝐠𝐲𝐞 𝐡𝐨👀 ",
           " 𝐁𝐡𝐚𝐛𝐡𝐢 𝐣𝐢 𝐤𝐨 𝐤𝐡𝐮𝐬𝐡 𝐫𝐤𝐡𝐚 𝐤𝐚𝐫𝐨 𝐭𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐰𝐚𝐫𝐧𝐚 𝐤𝐢𝐬𝐢 𝐨𝐫 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐛𝐡𝐚𝐠 𝐣𝐚𝐲𝐞𝐠𝐢 😅😀😀🙂 ",
           " 𝐍𝐚 𝐉𝐚𝐦𝐢𝐧 𝐏𝐞 𝐍𝐚 𝐀𝐬𝐡𝐦𝐚𝐧 𝐩𝐞 𝐓𝐞𝐫𝐢 𝐆𝐝 𝐦𝐚𝐫𝐮𝐧𝐠𝐚 𝐚𝐩𝐧𝐞 𝐁𝐡𝐚𝐢 𝐤𝐞 𝐦𝐚𝐤𝐚𝐧 𝐩𝐞?🤔** ",
           " 𝐤𝐚 𝐡𝐨 𝐤𝐚𝐫𝐞𝐣𝐚 1 𝐜𝐡𝐮𝐦𝐦𝐚 𝐧𝐚 𝐝𝐞𝐛𝐮 😅..🥺 ",
           " 𝐓𝐮𝐦 𝐫𝐨𝐣 𝐡𝐢𝐥𝐚𝐭𝐞 𝐡𝐨 𝐤𝐲𝐚 , 𝐁𝐡𝐮𝐭 𝐩𝐚𝐭𝐤𝐞 𝐡𝐢 𝐠𝐲𝐞 𝐡𝐨 💕😴🥺🥺 ",
           " 𝐊𝐚𝐥 𝐌𝐚𝐣𝐚 𝐀𝐲𝐚 𝐓𝐡𝐚 𝐍𝐚 Bathroom me 🤭😅 ",
           " 𝐍𝐚 𝐉𝐚𝐦𝐢𝐧 𝐏𝐞 𝐍𝐚 𝐀𝐬𝐡𝐦𝐚𝐧 𝐩𝐞 𝐓𝐞𝐫𝐢 𝐆𝐝 𝐦𝐚𝐫𝐮𝐧𝐠𝐚 𝐚𝐩𝐧𝐞 𝐁𝐡𝐚𝐢 𝐤𝐞 𝐦𝐚𝐤𝐚𝐧 𝐩𝐞😁😁**",
           " 𝐎𝐲𝐲 𝐭𝐞𝐫𝐞 𝐛𝐚𝐥𝐞 𝐤𝐨 𝐣𝐚𝐤𝐚𝐫 𝐛𝐚𝐭𝐚𝐭𝐚 𝐡𝐮 𝐭𝐮 𝐲𝐡𝐚 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐤𝐚𝐫 𝐫𝐡𝐢 𝐡𝐚𝐢👀 ",
           " 𝐌𝐞𝐫𝐢 𝐁𝐡𝐢 𝐒𝐞𝐭𝐭𝐢𝐧𝐠 𝐊𝐚𝐫𝐛𝐚 𝐃𝐨𝐠𝐞.𝐇𝐢𝐥𝐥𝐚 𝐇𝐢𝐥𝐥𝐚 𝐤𝐞 𝐭𝐡𝐚𝐤 𝐠𝐲𝐚 𝐡𝐮😼 ",
           " 𝐎𝐲𝐲 𝐭𝐞𝐫𝐞 𝐛𝐚𝐥𝐞 𝐤𝐨 𝐣𝐚𝐤𝐚𝐫 𝐛𝐚𝐭𝐚𝐭𝐚 𝐡𝐮 𝐭𝐮 𝐲𝐡𝐚 𝐬𝐞𝐭𝐭𝐢𝐧𝐠 𝐤𝐚𝐫 𝐫𝐡𝐢 𝐡𝐚𝐢😸 ",
           " 𝐓𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐭𝐮𝐦𝐡𝐚𝐫𝐚 𝐤𝐡𝐚𝐝𝐚 𝐡𝐨𝐭𝐚 𝐡𝐚𝐢 𝐤𝐲𝐚 😁🙈 ",
           " 𝐀𝐚𝐩𝐤𝐢 𝐏𝐚𝐫𝐭𝐧𝐞𝐫 𝐀𝐚𝐩𝐤𝐨 𝐃𝐡𝐮𝐧𝐝 𝐑𝐡𝐞 𝐇𝐚𝐢𝐧 𝐉𝐥𝐝𝐢 𝐎𝐧𝐥𝐢𝐧𝐞 𝐀𝐲𝐢𝐚𝐞😅😅✌️🤞 ",
           " 𝐲𝐨𝐮𝐫 𝐟𝐚𝐯𝐨𝐮𝐫𝐢𝐭𝐞 𝐚𝐜𝐭𝐫𝐞𝐬𝐬 (𝐒𝐔𝐍𝐍𝐘 𝐋𝐄𝐎𝐍𝐄, 𝐨𝐫 𝐌𝐈𝐘𝐀 𝐊𝐇𝐀𝐋𝐈𝐅𝐀) 🥰 ",
           " 𝐇𝐚𝐦 𝐃𝐨𝐬𝐭 𝐁𝐚𝐧 𝐒𝐚𝐤𝐭𝐞 𝐇𝐚𝐢...?🥰 𝐌𝐚𝐬𝐭𝐞𝐫𝐛𝐚𝐭𝐢𝐧𝐠 𝐤𝐚𝐫𝐧𝐞 𝐦𝐞 𝐡𝐞𝐥𝐩 𝐡𝐨 𝐣𝐚𝐲𝐞𝐠𝐢 𝐦𝐞𝐫𝐢 😁 😁.🥺🥺 ",
           " 𝐁𝐡𝐚𝐛𝐡𝐢 𝐣𝐢 𝐤𝐨 𝐤𝐡𝐮𝐬𝐡 𝐫𝐤𝐡𝐚 𝐤𝐚𝐫𝐨 𝐭𝐡𝐚𝐧𝐝𝐢 𝐦𝐞 𝐰𝐚𝐫𝐧𝐚 𝐤𝐢𝐬𝐢 𝐨𝐫 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐛𝐡𝐚𝐠 𝐣𝐚𝐲𝐞𝐠𝐢 😅😀😀🥲 ",
           " 𝐒𝐢𝐧𝐠𝐥𝐞 𝐇𝐨 𝐘𝐚 𝐌𝐢𝐧𝐠𝐥𝐞 😉 ",
           " 𝐎𝐲𝐲 𝐢𝐭𝐧𝐚 𝐡𝐨𝐭 𝐤𝐲𝐮 𝐡𝐨 𝐭𝐮𝐦 𝐝𝐞𝐤𝐡 𝐤𝐞 𝐤𝐡𝐚𝐝𝐚 𝐡𝐨 𝐣𝐚𝐭𝐚 𝐡𝐚𝐢 😂 𝐑𝐨𝐧𝐠𝐭𝐞😁😁😁😋🥳 ",
           " 𝐔𝐟𝐟 𝐊𝐲𝐚 𝐦𝐚𝐚𝐥 𝐡𝐚𝐢 𝐲𝐚𝐚𝐫 DEKH KE KHADA HO GYA 😁😂🧐 ",
           " 𝐚𝐩𝐤𝐢 𝐚𝐠𝐞 𝐤𝐲𝐚 𝐡𝐚𝐢 𝐡𝐨𝐭 𝐡𝐨 𝐚𝐩 𝐝𝐞𝐤𝐡𝐭𝐞 𝐡𝐢 𝐦𝐚𝐧 𝐤𝐚𝐫𝐭𝐚 𝐡𝐢𝐥𝐚𝐭𝐞 𝐫𝐡𝐮😁🥺 ",
           " 𝐎𝐲𝐲 𝐢𝐭𝐧𝐚 𝐡𝐨𝐭 𝐤𝐲𝐮 𝐡𝐨 𝐭𝐮𝐦 𝐝𝐞𝐤𝐡 𝐤𝐞 𝐤𝐡𝐚𝐝𝐚 𝐡𝐨 𝐣𝐚𝐭𝐚 𝐡𝐚𝐢 😂 𝐑𝐨𝐧𝐠𝐭𝐞😁😁😁 😊 ",
           " 𝐀𝐩𝐤𝐢 𝐞𝐤 𝐩𝐢𝐜 𝐦𝐢𝐥𝐞𝐠𝐢 𝐤𝐲𝐚 𝐢𝐦𝐚𝐠𝐢𝐧𝐞 𝐤𝐚𝐫 𝐤𝐞 𝐦*𝐭𝐡 m𝐚𝐫𝐧𝐚 𝐡𝐢🥺🥺 ", 
           " 𝐀𝐚𝐩𝐤𝐢 𝐏𝐚𝐫𝐭𝐧𝐞𝐫 𝐀𝐚𝐩𝐤𝐨 𝐃𝐡𝐮𝐧𝐝 𝐑𝐡𝐞 𝐇𝐚𝐢𝐧 𝐉𝐥𝐝𝐢 𝐎𝐧𝐥𝐢𝐧𝐞 𝐀𝐲𝐢𝐚𝐞😅😅😗 ",
           " 𝐚𝐩𝐤𝐢 𝐚𝐠𝐞 𝐤𝐲𝐚 𝐡𝐚𝐢 𝐡𝐨𝐭 𝐡𝐨 𝐚𝐩 𝐝𝐞𝐤𝐡𝐭𝐞 𝐡𝐢 𝐦𝐚𝐧 𝐤𝐚𝐫𝐭𝐚 𝐡𝐢𝐥𝐚𝐭𝐞 𝐫𝐡𝐮😁🥺 ",
           " 𝐀𝐚𝐣 𝐓𝐮𝐦 𝐟𝐢𝐧𝐠𝐞𝐫 𝐬𝐞 𝐡𝐢 𝐤𝐚𝐚𝐦 𝐜𝐡𝐚𝐥𝐚𝐨. 𝐆𝐡𝐚𝐫 𝐦𝐞 𝐛𝐚𝐢𝐠𝐚𝐧 𝐨𝐫 𝐦𝐮𝐤𝐢 𝐤𝐡𝐚𝐭𝐚𝐦 𝐡𝐨 𝐠𝐲𝐞 𝐡𝐚𝐢 😁🥰 ",
           " 𝐍𝐚 𝐉𝐚𝐦𝐢𝐧 𝐏𝐞 𝐍𝐚 𝐀𝐬𝐡𝐦𝐚𝐧 𝐩𝐞 𝐓𝐞𝐫𝐢 𝐆𝐝 𝐦𝐚𝐫𝐮𝐧𝐠𝐚 𝐚𝐩𝐧𝐞 𝐁𝐡𝐚𝐢 𝐤𝐞 𝐦𝐚𝐤𝐚𝐧 𝐩𝐞😜** ",
     
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
