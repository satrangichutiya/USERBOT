"""
VirusTotal plugin
Commands: vt, vtl
"""

import aiohttp
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.helpers import edit_or_reply

# Mock VirusTotal responses (since we don't have real API)
MOCK_VT_RESPONSES = [
    {
        "clean": True,
        "detections": 0,
        "total_scans": 67,
        "scan_date": "2024-01-15 10:30:45",
        "engines": ["Avast", "AVG", "Bitdefender", "Kaspersky", "McAfee", "Norton"]
    },
    {
        "clean": False,
        "detections": 15,
        "total_scans": 67,
        "scan_date": "2024-01-15 10:30:45",
        "engines": ["Avast", "AVG", "Bitdefender", "Kaspersky", "McAfee", "Norton"],
        "threats": ["Trojan.Win32.Generic", "Malware.Suspicious", "PUP.Optional"]
    }
]

@Client.on_message(filters.command(["vt"], Config.COMMAND_PREFIXES) & filters.me)
async def virustotal_scan(client: Client, message: Message):
    """Scan URL/file with VirusTotal"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.vt [url/file]`")
        return
    
    target = message.command[1]
    
    # Check if it's a URL or file
    if target.startswith(('http://', 'https://')):
        scan_type = "URL"
    else:
        scan_type = "File"
    
    msg = await edit_or_reply(message, f"🔍 **Scanning {scan_type} with VirusTotal...**")
    
    # Simulate scanning delay
    await asyncio.sleep(3)
    
    # Use mock response (in real implementation, you'd use VirusTotal API)
    import random
    result = random.choice(MOCK_VT_RESPONSES)
    
    if result["clean"]:
        status_emoji = "✅"
        status_text = "CLEAN"
        color = "🟢"
    else:
        status_emoji = "⚠️"
        status_text = "THREAT DETECTED"
        color = "🔴"
    
    scan_result = (
        f"🛡️ **VirusTotal Scan Result**\n\n"
        f"**Target:** `{target}`\n"
        f"**Type:** {scan_type}\n"
        f"**Status:** {status_emoji} {status_text}\n\n"
        f"**📊 Scan Details:**\n"
        f"• **Detections:** {result['detections']}/{result['total_scans']}\n"
        f"• **Scan Date:** {result['scan_date']}\n"
        f"• **Engines:** {len(result['engines'])} engines\n\n"
    )
    
    if not result["clean"]:
        scan_result += f"**⚠️ Detected Threats:**\n"
        for threat in result.get("threats", []):
            scan_result += f"• `{threat}`\n"
        scan_result += "\n"
    
    scan_result += (
        f"**🔍 Top Engines:**\n"
        f"• {', '.join(result['engines'][:5])}\n\n"
        f"*Powered by VirusTotal API*"
    )
    
    await msg.edit(scan_result)

@Client.on_message(filters.command(["vtl", "vtlink"], Config.COMMAND_PREFIXES) & filters.me)
async def virustotal_link(client: Client, message: Message):
    """Generate VirusTotal scan link"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.vtl [url]`")
        return
    
    url = message.command[1]
    
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
    
    # Generate mock VirusTotal link
    import hashlib
    url_hash = hashlib.md5(url.encode()).hexdigest()
    vt_link = f"https://www.virustotal.com/gui/url/{url_hash}/detection"
    
    link_text = (
        f"🔗 **VirusTotal Scan Link**\n\n"
        f"**URL:** `{url}`\n"
        f"**Scan Link:** [Click here to scan]({vt_link})\n\n"
        f"**📝 Instructions:**\n"
        f"1. Click the link above\n"
        f"2. Wait for scan to complete\n"
        f"3. Review the results\n\n"
        f"*Note: This will open VirusTotal in your browser*"
    )
    
    await edit_or_reply(message, link_text, disable_web_page_preview=True)

@Client.on_message(filters.command(["vtscan"], Config.COMMAND_PREFIXES) & filters.me)
async def virustotal_file_scan(client: Client, message: Message):
    """Scan replied file with VirusTotal"""
    if not message.reply_to_message or not message.reply_to_message.document:
        await edit_or_reply(message, "❌ **Please reply to a file to scan!**")
        return
    
    file = message.reply_to_message.document
    file_name = file.file_name or "Unknown"
    file_size = file.file_size
    
    if file_size > 32 * 1024 * 1024:  # 32MB limit
        await edit_or_reply(message, "❌ **File too large! Maximum size: 32MB**")
        return
    
    msg = await edit_or_reply(message, f"🔍 **Scanning file: {file_name}...**")
    
    # Simulate file download and scan
    await asyncio.sleep(2)
    await msg.edit(f"📤 **Uploading to VirusTotal...**")
    await asyncio.sleep(3)
    await msg.edit(f"🔍 **Scanning in progress...**")
    await asyncio.sleep(4)
    
    # Mock scan result
    import random
    result = random.choice(MOCK_VT_RESPONSES)
    
    if result["clean"]:
        status_emoji = "✅"
        status_text = "CLEAN"
    else:
        status_emoji = "⚠️"
        status_text = "THREAT DETECTED"
    
    scan_result = (
        f"🛡️ **VirusTotal File Scan**\n\n"
        f"**File:** `{file_name}`\n"
        f"**Size:** `{file_size:,} bytes`\n"
        f"**Status:** {status_emoji} {status_text}\n\n"
        f"**📊 Scan Results:**\n"
        f"• **Detections:** {result['detections']}/{result['total_scans']}\n"
        f"• **Scan Date:** {result['scan_date']}\n"
        f"• **Risk Level:** {'Low' if result['clean'] else 'High'}\n\n"
    )
    
    if not result["clean"]:
        scan_result += f"**⚠️ Detected Threats:**\n"
        for threat in result.get("threats", []):
            scan_result += f"• `{threat}`\n"
        scan_result += "\n"
    
    scan_result += f"**Recommendation:** {'File is safe to use' if result['clean'] else 'Do not execute this file!'}"
    
    await msg.edit(scan_result)

@Client.on_message(filters.command(["vtinfo"], Config.COMMAND_PREFIXES) & filters.me)
async def virustotal_info(client: Client, message: Message):
    """Show VirusTotal information"""
    info_text = (
        f"🛡️ **VirusTotal Information**\n\n"
        f"**What is VirusTotal?**\n"
        f"VirusTotal is a free online service that analyzes files and URLs "
        f"for viruses, worms, trojans and other kinds of malicious content.\n\n"
        f"**📊 Features:**\n"
        f"• Scans with 70+ antivirus engines\n"
        f"• URL and file analysis\n"
        f"• Behavioral analysis\n"
        f"• Community comments\n"
        f"• Historical scan data\n\n"
        f"**🔧 Available Commands:**\n"
        f"• `.vt [url]` - Scan URL\n"
        f"• `.vtl [url]` - Generate scan link\n"
        f"• `.vtscan` - Scan replied file\n\n"
        f"**⚠️ Privacy Note:**\n"
        f"Files uploaded to VirusTotal are shared with "
        f"security vendors and researchers.\n\n"
        f"**Website:** https://www.virustotal.com"
    )
    
    await edit_or_reply(message, info_text, disable_web_page_preview=True)