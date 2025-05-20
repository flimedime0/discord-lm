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
6. Set `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` in `.env` for web search.

## Running

Run the bot using Python:

```bash
python bot.py
```

The bot uses OpenAI's `o3` model by default. Parameters for the current model are
configured in `DEFAULT_PARAMS` within `bot.py` and can be overridden using
environment variables like `OAI_TEMPERATURE` and `OAI_MAX_TOKENS`.
When the bot is running, mention it with a question (e.g. `@YourBot what is 2+2?`)
or use the `/chat` slash command to talk to it. The `/options` command lets you
switch between the `o3` and `4o` models and adjust parameters at runtime.
- If configured with Google credentials, the bot may search the web via Google Custom Search when it needs additional context. Manual search commands are not supported.

## GitHub Codespaces Quick Start

This repository includes a devcontainer so you can get up and running with one click.
Create a codespace and then:

```bash
cp .env.example .env
# edit .env and add your tokens
python bot.py
```

## Quick Start

```bash
git clone <repo-url>
cd discord-lm-app
cp .env.example .env
python bot.py
```

## Data Flow

Discord message → bot → OpenAI → Google CSE → Discord.

## Environment Variables

| Name | Purpose |
|------|---------|
| `DISCORD_TOKEN` | Discord bot token |
| `OPENAI_API_KEY` | OpenAI API key |
| `GOOGLE_API_KEY` | Google API key |
| `GOOGLE_CSE_ID` | Google Custom Search Engine ID |
| `OAI_TEMPERATURE` | OpenAI model temperature |
| `OAI_TOP_P` | Nucleus sampling top_p |
| `OAI_MAX_TOKENS` | Max tokens for responses |
| `OAI_STOP` | Stop sequence |
| `OAI_SEED` | Integer seed for the model |
| `OAI_MODEL` | Default model (`o3` or `4o`) |

## Message Length Handling

Responses are split into 2 000-character chunks. URLs are never cut in half.
If a chunk ends in the middle of a word, the bot backs up to the previous
space or period. A new placeholder message is created only when there is more
content so blank `...` messages are avoided.
