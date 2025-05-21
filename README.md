# Discord ChatGPT Bot

![Python 3.11](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Black](https://img.shields.io/badge/code%20style-black-000000)
![CI](https://github.com/<USER>/discord-lm-app/actions/workflows/ci.yml/badge.svg)
![Docs](https://img.shields.io/badge/docs-site-blue)
![Coverage](https://codecov.io/gh/flimedime0/discord-lm-app/branch/main/graph/badge.svg)
![Release](https://img.shields.io/github/v/release/flimedime0/discord-lm-app)

**• [CONTRIBUTING](CONTRIBUTING.md)** – dev setup & workflow  
**• [Project state](PROJECT_STATE.md)** – architecture & roadmap

This repository contains a simple Discord bot that connects to the OpenAI ChatGPT API. When a user @-mentions the bot, e.g. `@YourBot what is 2+2?`, the bot forwards the prompt to ChatGPT and replies with the response. The bot replies whenever it's mentioned in a message.
Full documentation → <https://flimedime0.github.io/discord-lm-app/>

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

### Quick start with Docker

```bash
docker compose up --build -d        # first run
docker compose logs -f bot          # view logs
```

## Package Layout

The bot code resides in `src/discord_lm_bot/`. Run the bot via `discord_lm_bot.run_bot`
or import `discord_lm_bot.query_chatgpt` for custom integrations.

## Running

Run the bot using Python:

```bash
python bot.py
```

The bot uses OpenAI's `o3` model by default. Parameters for this model are
configured in `DEFAULT_O3_PARAMS` within `bot.py`.
When the bot is running, mention it with a question (e.g. `@YourBot what is 2+2?`) and it will reply.
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
pre-commit install  # devcontainer does this automatically
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

## Message Length Handling

Responses are split into 2 000-character chunks. URLs are never cut in half.
If a chunk ends in the middle of a word, the bot backs up to the previous
space or period. A new placeholder message is created only when there is more
content so blank `...` messages are avoided.

## Formatted with Black & Ruff

This project uses [Black](https://github.com/psf/black) and
[Ruff](https://github.com/astral-sh/ruff) for automatic formatting and linting.
