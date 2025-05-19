# Discord ChatGPT Bot

This repository contains a simple Discord bot that connects to the OpenAI ChatGPT API. When a user types `!ask <your question>` in a Discord channel, the bot forwards the prompt to ChatGPT and replies with the response.

## Setup

1. Install Python 3.7+ and the dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a Discord application and bot in the [Discord Developer Portal](https://discord.com/developers/applications). Copy the bot token.
3. Obtain an OpenAI API key.
4. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   # then edit .env to add your tokens
   ```

## Running

Run the bot using Python:

```bash
python bot.py
```

The bot uses OpenAI's `gpt-4o` model with `temperature=1` and `top_p=0` by default.
When the bot is running, send messages starting with `!ask` to interact with ChatGPT.

## GitHub Codespaces Quick Start

This repository includes a devcontainer so you can get up and running with one click.
Create a codespace and then:

```bash
cp .env.example .env
# edit .env and add your tokens
python bot.py
```
