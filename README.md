# AI Lab Discord Bot

A feature-rich Discord bot built with Python and discord.py. It combines moderation, utility commands, AI-powered chat, and simple automation into a clean, modular project structure.

## Overview

This bot is designed to be a practical, production-ready Discord assistant for servers that want:

- moderation tools for admins
- fun and utility commands for regular users
- AI-powered replies through a Groq/OpenAI-compatible API
- easy extensibility through cogs

It is organized in a clean way so it can be expanded later with more features, slash commands, logging, or persistent storage.

---

## Features

### Moderation
The bot includes several moderation features for server administrators:

- `!kick @user [reason]` — kick a user from the server
- `!ban @user [reason]` — ban a user from the server
- `!unban [user_id]` — unban a user by their Discord ID
- `!clear [number]` — delete a number of recent messages from the current channel
- `!mute @user [duration]` — mute a user indefinitely or for a timed duration
- `!unmute @user` — remove the mute role from a user

Timed mute examples:

```text
!mute @user 10m
!mute @user 1h
!mute @user 1d
```

### Utility and Fun
The bot also supports useful community commands:

- `!ping` — check bot latency
- `!serverinfo` — show server information
- `!userinfo @user` — show user information and roles
- `!poll [question]` — create a simple yes/no poll with reactions
- Welcome messages for new members in the `general` channel

### AI Chat
The bot has an AI-powered command:

- `!ask [question]` — answer a question using the configured AI provider

If the AI service is unavailable, the bot falls back to a helpful built-in response so it still behaves gracefully.

---

## Project Structure

```text
Ai_Lab/
├── .env                  # Environment variables for token and AI config
├── .gitignore            # Git ignore rules
├── .venv/                # Virtual environment
├── cogs/                 # Bot feature modules
│   ├── ai.py             # AI chat command
│   ├── fun.py            # Utility and fun commands
│   ├── moderation.py    # Moderation commands
│   └── __init__.py       # Package marker
├── main.py               # Main Discord bot entrypoint
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── tests/                # Automated tests
└── PROJECT_ANALYSIS.md   # Detailed architecture breakdown
```

---

## Requirements

Make sure you have Python 3.10+ installed.

Install the required dependencies:

```bash
pip install -r requirements.txt
```

If you are using the included virtual environment, you can activate it and run:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root with the following values:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1
```

### Notes
- The bot token must come from the Discord Developer Portal.
- The AI features use the Groq/OpenAI-compatible endpoint configured in the `.env` file.
- Keep your `.env` file private and never commit it to GitHub.

---

## How to Run the Bot

From the project folder, run:

```bash
python main.py
```

If you are using the virtual environment explicitly, run:

```bash
.venv\Scripts\python.exe main.py
```

When the bot starts successfully, you should see output similar to:

```text
Logged in as Ai_Lab_Bot#4213
The bot is ready to serve.
```

---

## Discord Permissions Needed

To ensure the bot works properly, make sure it has the following permissions in your server:

- View Channels
- Send Messages
- Read Message History
- Manage Messages
- Kick Members
- Ban Members
- Manage Roles

Without these permissions, features such as moderation and welcome messaging may not work as expected.

---

## Commands to Test in Discord

You can test the bot in a Discord text channel using the following commands:

### Basic Commands

```text
!ping
!serverinfo
!userinfo @yourname
!poll Is the bot working?
```

### AI Commands

```text
!ask Hello
!ask What is Python?
```

### Moderation Commands

Only use these if you have permission:

```text
!clear 5
!kick @user
!ban @user
!unban 123456789012345678
!mute @user 10m
!unmute @user
```

---

## Architecture Overview

The project uses a modular architecture built around Discord cogs.

### How it works
1. `main.py` creates the Discord bot instance and loads the cogs.
2. The cogs provide separate command groups:
   - moderation logic in `cogs/moderation.py`
   - utility and fun commands in `cogs/fun.py`
   - AI chat behavior in `cogs/ai.py`
3. The bot receives user messages and dispatches them to the correct command handler.
4. Responses are sent back to Discord as messages or embeds.

This structure makes it easier to extend the bot later with more features without cluttering the main file.

---

## Error Handling and Reliability

The bot includes:

- graceful handling for missing permissions
- helpful error messages for incorrect command usage
- cooldowns to reduce spam and abuse
- fallback AI responses when the external API is unavailable

These features make the bot more robust and user-friendly in real Discord servers.

---

## Testing

The project includes a basic automated test suite under the `tests/` folder.

You can run the tests with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

This helps verify that core bot behaviors still work properly after updates.

---

## Deployment Notes

This bot can be run locally for development or deployed to a remote environment such as:

- a VPS
- a cloud VM
- a containerized host
- a PaaS that supports Python processes

For production use, it is recommended to:

- store secrets in a secure environment manager rather than hardcoding them
- run the bot with a process manager such as `systemd` or Docker
- enable logging and monitoring
- keep dependencies updated

---

## Future Improvements

Possible future enhancements include:

- slash commands for modern Discord interactions
- persistent moderation logs
- role-based command permissions
- database-backed settings and warnings
- additional AI features such as conversation memory
- support for more advanced moderation workflows

---

## Summary

This project is a practical Discord bot that combines moderation, utility tools, AI chat, and automation into one extensible Python application. It is suitable for learning, experimentation, and real-world server use.

If you want to contribute or expand it further, the modular structure makes it straightforward to add new commands and features.
