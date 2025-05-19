# Discord ChatGPT Bot

This repository contains a simple Discord bot that connects to the OpenAI ChatGPT API. When a user types `!ask <your question>` in a Discord channel, the bot forwards the prompt to ChatGPT and replies with the response.

## Setup

1. Install Python 3.7+ and install dependencies:
   ```bash
   pip install discord.py openai
   ```
2. Create a Discord application and bot in the [Discord Developer Portal](https://discord.com/developers/applications). Copy the bot token.
3. Obtain an OpenAI API key.
4. Set the `DISCORD_TOKEN` and `OPENAI_API_KEY` environment variables before running the bot:
   ```bash
   export DISCORD_TOKEN=your-discord-bot-token
   export OPENAI_API_KEY=your-openai-api-key
   ```

## Running

Run the bot using Python:

```bash
python bot.py
```

When the bot is running, send messages starting with `!ask` to interact with ChatGPT.
