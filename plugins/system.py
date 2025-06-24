"""
System commands plugin
Commands: status, prefix, setprefix, sendmod, autokill
"""

import psutil
import platform
import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.helpers import edit_or_reply, get_readable_time, get_size
from utils.database import Database

db = Database()

@Client.on_message(filters.command(["status"], Config.COMMAND_PREFIXES) & filters.me)
async def system_status(client: Client, message: Message):
    """Show fake server stats for fun/dev trolling"""
    import random
    
    # Generate fake but realistic looking stats
    fake_stats = {
        'cpu_cores': random.randint(8, 64),
        'cpu_usage': random.uniform(15.0, 85.0),
        'ram_total': random.randint(16, 128),
        'ram_used': random.uniform(30.0, 70.0),
        'disk_total': random.randint(500, 2000),
        'disk_used': random.uniform(40.0, 80.0),
        'network_up': random.uniform(100.0, 1000.0),
        'network_down': random.uniform(500.0, 2000.0),
        'uptime_days': random.randint(1, 365),
        'processes': random.randint(200, 500),
        'temperature': random.randint(35, 75)
    }
    
    status_text = (
        f"🖥️ **Moon Server Status**\n\n"
        f"**🔧 System Info:**\n"
        f"• OS: Ubuntu 22.04 LTS\n"
        f"• Kernel: 5.15.0-moon-server\n"
        f"• Architecture: x86_64\n"
        f"• Hostname: moon-prod-{random.randint(1, 99)}\n\n"
        
        f"**⚡ Performance:**\n"
        f"• CPU: {fake_stats['cpu_cores']} cores @ {fake_stats['cpu_usage']:.1f}%\n"
        f"• RAM: {fake_stats['ram_used']:.1f}% of {fake_stats['ram_total']}GB\n"
        f"• Disk: {fake_stats['disk_used']:.1f}% of {fake_stats['disk_total']}GB\n"
        f"• Temperature: {fake_stats['temperature']}°C\n\n"
        
        f"**🌐 Network:**\n"
        f"• Upload: {fake_stats['network_up']:.1f} Mbps\n"
        f"• Download: {fake_stats['network_down']:.1f} Mbps\n"
        f"• Latency: {random.randint(1, 15)}ms\n\n"
        
        f"**📊 Runtime:**\n"
        f"• Uptime: {fake_stats['uptime_days']} days\n"
        f"• Processes: {fake_stats['processes']}\n"
        f"• Load Average: {random.uniform(0.5, 3.0):.2f}\n"
        f"• Last Reboot: {random.randint(1, 30)} days ago\n\n"
        
        f"**🔒 Security:**\n"
        f"• Firewall: ✅ Active\n"
        f"• SSL: ✅ Valid\n"
        f"• DDoS Protection: ✅ Enabled\n"
        f"• Intrusion Detection: ✅ Active\n\n"
        
        f"*Status as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*"
    )
    
    await edit_or_reply(message, status_text)

@Client.on_message(filters.command(["sp", "setprefix"], Config.COMMAND_PREFIXES) & filters.me)
async def set_prefix(client: Client, message: Message):
    """Set command prefix"""
    if len(message.command) < 2:
        current_prefix = await db.get_user_data(message.from_user.id)
        prefix = current_prefix.get('prefix', Config.DEFAULT_PREFIX)
        await edit_or_reply(message, f"🔧 **Current prefix:** `{prefix}`\n\n**Usage:** `.sp [new_prefix]`")
        return
    
    new_prefix = message.command[1]
    
    if len(new_prefix) > 5:
        await edit_or_reply(message, "❌ **Prefix too long! Maximum 5 characters.**")
        return
    
    await db.set_user_data(message.from_user.id, {'prefix': new_prefix})
    await edit_or_reply(message, f"✅ **Prefix changed to:** `{new_prefix}`")

@Client.on_message(filters.command(["sendmod"], Config.COMMAND_PREFIXES) & filters.me)
async def send_module(client: Client, message: Message):
    """Send module file"""
    if len(message.command) < 2:
        await edit_or_reply(message, "❌ **Usage:** `.sendmod [module_name]`")
        return
    
    module_name = message.command[1].lower()
    
    try:
        # Try to find and send the module file
        import os
        module_path = f"plugins/{module_name}.py"
        
        if os.path.exists(module_path):
            await message.reply_document(
                module_path,
                caption=f"📄 **Module:** `{module_name}.py`\n\n🌙 **Moon UserBot Module**"
            )
            await message.delete()
        else:
            await edit_or_reply(message, f"❌ **Module not found:** `{module_name}`")
    
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** `{str(e)}`")

@Client.on_message(filters.command(["autokill"], Config.COMMAND_PREFIXES) & filters.me)
async def auto_kill(client: Client, message: Message):
    """Auto kill/restart system (fake)"""
    import random
    import asyncio
    
    kill_messages = [
        "🔥 **INITIATING AUTO-KILL SEQUENCE...**",
        "💀 **TERMINATING ALL PROCESSES...**",
        "⚡ **SYSTEM SHUTDOWN INITIATED...**",
        "🌪️ **NUCLEAR OPTION ACTIVATED...**",
        "💥 **SELF-DESTRUCT SEQUENCE STARTED...**"
    ]
    
    msg = await edit_or_reply(message, random.choice(kill_messages))
    await asyncio.sleep(2)
    
    await msg.edit("🔄 **KILLING PROCESSES:**\n\n"
                   "• nginx ✅\n"
                   "• mysql ✅\n"
                   "• redis ✅\n"
                   "• mongodb ✅")
    await asyncio.sleep(2)
    
    await msg.edit("💀 **SYSTEM TERMINATED!**\n\n"
                   "🔄 **Auto-restart in 3 seconds...**")
    await asyncio.sleep(3)
    
    await msg.edit("✅ **SYSTEM RESTARTED SUCCESSFULLY!**\n\n"
                   "🌙 **Moon UserBot is back online!**\n"
                   f"⏰ **Restart time:** {datetime.now().strftime('%H:%M:%S')}")

@Client.on_message(filters.command(["sysinfo"], Config.COMMAND_PREFIXES) & filters.me)
async def system_info(client: Client, message: Message):
    """Show real system information"""
    # Get real system stats
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = psutil.boot_time()
    uptime = get_readable_time(int(time.time() - boot_time))
    
    system_info = (
        f"💻 **Real System Information**\n\n"
        f"**🔧 System:**\n"
        f"• Platform: {platform.system()} {platform.release()}\n"
        f"• Architecture: {platform.machine()}\n"
        f"• Processor: {platform.processor()}\n"
        f"• Python: {platform.python_version()}\n\n"
        
        f"**📊 Performance:**\n"
        f"• CPU Usage: {cpu_percent}%\n"
        f"• RAM: {memory.percent}% ({get_size(memory.used)}/{get_size(memory.total)})\n"
        f"• Disk: {disk.percent}% ({get_size(disk.used)}/{get_size(disk.total)})\n"
        f"• Uptime: {uptime}\n\n"
        
        f"**🌙 Moon UserBot:**\n"
        f"• Version: 3.4.5\n"
        f"• Pyrogram: Latest\n"
        f"• Status: ✅ Running"
    )
    
    await edit_or_reply(message, system_info)

@Client.on_message(filters.command(["modules", "plugins"], Config.COMMAND_PREFIXES) & filters.me)
async def list_modules(client: Client, message: Message):
    """List all loaded modules"""
    import os
    
    plugin_files = [f[:-3] for f in os.listdir('plugins') if f.endswith('.py') and not f.startswith('_')]
    plugin_count = len(plugin_files)
    
    modules_text = (
        f"🔧 **Loaded Modules ({plugin_count}):**\n\n"
    )
    
    # Group modules by category
    categories = {
        'Core': ['basic', 'system'],
        'Fun': ['fun'],
        'Admin': ['admin'],
        'Utility': ['filters', 'notes', 'userinfo'],
        'Media': [],
        'Social': [],
        'Security': [],
        'AI': []
    }
    
    for category, modules in categories.items():
        if modules:
            modules_text += f"**{category}:**\n"
            for module in modules:
                if module in plugin_files:
                    modules_text += f"• {module}\n"
            modules_text += "\n"
    
    # Add remaining modules
    other_modules = [m for m in plugin_files if not any(m in cat_modules for cat_modules in categories.values())]
    if other_modules:
        modules_text += "**Other:**\n"
        for module in other_modules:
            modules_text += f"• {module}\n"
    
    modules_text += f"\n**Total Modules:** `{plugin_count}`"
    
    await edit_or_reply(message, modules_text)