# Discord ChatGPT Bot

This repository contains a simple Discord bot that connects to the OpenAI ChatGPT API. When a user @-mentions the bot, e.g. `@YourBot what is 2+2?`, the bot forwards the prompt to ChatGPT and replies with the response. The bot replies whenever it's mentioned in a message.

## Setup

1. Install Python 3.7+ and the dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a Discord application and bot in the [Discord Developer Portal](https://discord.com/developers/applications). Copy the bot token.
3. In the **Bot** tab of the Developer Portal, enable the **Message Content Intent** so the bot can read message contents.
4. Obtain an OpenAI API key.
5. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   # then edit .env to add your tokens
   ```
5. Set `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` in `.env` for web search.

## Running

Run the bot using Python:

```bash
python bot.py
```

The bot uses OpenAI's `o3` model by default. Parameters for this model are
configured in `DEFAULT_O3_PARAMS` within `bot.py`.
When the bot is running, mention it with a question (e.g. `@YourBot what is 2+2?`) and it will reply.
- The bot can search the web via Google Custom Search. To force a web search, start your question with `search the internet` followed by the query.

## GitHub Codespaces Quick Start

This repository includes a devcontainer so you can get up and running with one click.
Create a codespace and then:

```bash
cp .env.example .env
# edit .env and add your tokens
python bot.py
```
