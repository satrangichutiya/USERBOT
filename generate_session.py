#!/usr/bin/env python3
"""
Session String Generator for Moon UserBot
"""

from pyrogram import Client
import asyncio

async def generate_session():
    """Generate Pyrogram session string"""
    print("🌙 Moon UserBot - Session String Generator")
    print("=" * 50)
    
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API HASH: ")
    
    if not api_id or not api_hash:
        print("❌ API ID and API HASH are required!")
        return
    
    try:
        api_id = int(api_id)
    except ValueError:
        print("❌ API ID must be a number!")
        return
    
    print("\n📱 Please enter your phone number when prompted...")
    print("🔐 You will receive an OTP, enter it when asked...")
    print("⚠️  If you have 2FA enabled, you'll need to enter your password too...")
    
    async with Client("moon_session", api_id=api_id, api_hash=api_hash) as app:
        session_string = await app.export_session_string()
        
        print("\n" + "=" * 50)
        print("✅ Session string generated successfully!")
        print("=" * 50)
        print(f"SESSION_STRING = {session_string}")
        print("=" * 50)
        print("\n📝 Copy the above session string and paste it in your .env file")
        print("🔒 Keep this session string safe and don't share it with anyone!")
        print("🌙 Moon UserBot setup is almost complete!")

if __name__ == "__main__":
    asyncio.run(generate_session())