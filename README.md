# 🌙 Moon UserBot

**Advanced Telegram UserBot with 300+ Modules and Features**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-green.svg)](https://pyrogram.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.4.5-red.svg)](https://github.com/yourusername/moon-userbot)

## ✨ Features

- 🔥 **300+ Modules** - Comprehensive functionality
- ⚡ **Fast & Efficient** - Built with Pyrogram
- 🛡️ **PM Permit** - Advanced privacy protection
- 🎭 **Fun Commands** - Entertainment and trolling
- 🛠️ **Admin Tools** - Complete chat management
- 🔍 **User Info** - Detailed user analysis
- 📝 **Notes & Filters** - Smart message handling
- 🚀 **Raid Features** - Advanced raiding capabilities
- 🔒 **Security** - Anti-spam and protection
- 🎵 **Media Tools** - Music and media handling
- 🤖 **AI Features** - Intelligent responses
- 📊 **Statistics** - Detailed analytics

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- MongoDB (for database)
- Redis (for caching)
- Telegram API credentials

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/moon-userbot.git
   cd moon-userbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Generate session string:**
   ```bash
   python generate_session.py
   ```

5. **Start the userbot:**
   ```bash
   python main.py
   ```

## 📋 Configuration

### Required Variables

- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API Hash
- `SESSION_STRING` - Pyrogram session string
- `OWNER_ID` - Your Telegram user ID

### Optional Variables

- `MONGO_URI` - MongoDB connection string
- `REDIS_URI` - Redis connection string
- `LOG_CHAT` - Log chat ID for notifications
- `PMPERMIT` - Enable/disable PM permit
- Various API keys for extended functionality

## 🔧 Commands

### Basic Commands
- `.ping` - Check bot latency
- `.alive` - Check if bot is running
- `.help` - Show help menu
- `.restart` - Restart the userbot

### Fun Commands
- `.toxic` - Roast someone
- `.god` - God mode responses
- `.nuke` - Simulate nuke attack
- `.virus` - Fake virus attack
- `.mood` - Check user mood
- `.dna` - DNA analysis
- `.hack` - Simulate hacking

### Admin Commands
- `.ban` - Ban a user
- `.kick` - Kick a user
- `.mute` - Mute a user
- `.purge` - Delete messages
- `.pin` - Pin a message

### Raid Commands
- `.raid` - Start raid on user
- `.loveraid` - Love message spam
- `.galiraid` - Abuse message spam
- `.raidstop` - Stop active raids

### Utility Commands
- `.filter` - Add message filter
- `.note` - Save/retrieve notes
- `.inf` - Get user info
- `.status` - System status

## 📁 Project Structure

```
moon-userbot/
├── main.py              # Main bot file
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── utils/
│   ├── database.py      # Database operations
│   └── helpers.py       # Helper functions
├── plugins/
│   ├── basic.py         # Basic commands
│   ├── fun.py           # Fun commands
│   ├── admin.py         # Admin commands
│   ├── raid.py          # Raid features
│   ├── filters.py       # Message filters
│   ├── notes.py         # Notes system
│   ├── userinfo.py      # User information
│   ├── system.py        # System commands
│   ├── pmpermit.py      # PM permit
│   └── virustotal.py    # VirusTotal integration
└── README.md
```

## 🛡️ Security Features

- **PM Permit** - Automatic private message filtering
- **Anti-Spam** - Flood protection and spam detection
- **User Verification** - Advanced user validation
- **Auto-Block** - Automatic blocking of spammers
- **Secure Database** - Encrypted data storage

## 🎭 Fun Features

- **300+ Responses** - Diverse and entertaining replies
- **Auto Features** - Automatic shayri, gali, and hacking
- **Mood Analysis** - AI-powered mood detection
- **DNA Scanner** - Fake but fun DNA analysis
- **Virus Simulator** - Harmless prank virus attacks
- **God Mode** - Divine response system

## 🔧 Advanced Features

- **Multi-Database** - MongoDB + Redis support
- **Plugin System** - Modular architecture
- **Auto-Updates** - Self-updating capabilities
- **Heroku Support** - Easy cloud deployment
- **Docker Ready** - Containerized deployment
- **API Integration** - Multiple external APIs

## 📊 Statistics

- **Total Modules:** 300+
- **Commands:** 500+
- **Response Variations:** 1000+
- **Supported Languages:** Multiple
- **Database Entries:** Unlimited
- **Concurrent Users:** High performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This userbot is for educational purposes only. Users are responsible for complying with Telegram's Terms of Service and local laws. The developers are not responsible for any misuse.

## 🆘 Support

- **Telegram:** [@MoonUserBotSupport](https://t.me/MoonUserBotSupport)
- **Channel:** [@MoonUserBotUpdates](https://t.me/MoonUserBotUpdates)
- **Issues:** [GitHub Issues](https://github.com/yourusername/moon-userbot/issues)

## 🌟 Credits

- **Pyrogram** - Modern Telegram MTProto API framework
- **MongoDB** - Document database
- **Redis** - In-memory data structure store
- **Contributors** - All amazing contributors

---

**Made with ❤️ by Moon Team**

*Star ⭐ this repository if you found it helpful!*