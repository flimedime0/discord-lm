# Discord ChatGPT Bot

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue)](https://github.com/flimedime0/discord-lm-app)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/flimedime0/discord-lm-app/blob/main/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)
[![CI](https://github.com/flimedime0/discord-lm-app/actions/workflows/ci.yml/badge.svg)](https://github.com/flimedime0/discord-lm-app/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-site-blue)](https://flimedime0.github.io/discord-lm-app/)
[![Coverage](https://codecov.io/gh/flimedime0/discord-lm-app/branch/main/graph/badge.svg)](https://codecov.io/gh/flimedime0/discord-lm-app)
[![Release](https://img.shields.io/github/v/release/flimedime0/discord-lm-app)](https://github.com/flimedime0/discord-lm-app/releases)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io%2Fflimedime0%2Fdiscord--lm--app-blue)](https://github.com/flimedime0/discord-lm-app/pkgs/container/discord-lm-app)

**• [CONTRIBUTING](CONTRIBUTING.md)** – dev setup & workflow
**• [Project state](PROJECT_STATE.md)** – architecture & roadmap

A lightweight Discord bot that talks to OpenAI's ChatGPT models. Mention the bot in a server and it responds using the `o3` model by default. If Google credentials are configured, it can search the web for up-to-date information and cite the sources in its replies.

Full documentation → <https://flimedime0.github.io/discord-lm-app/>

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Development Workflow](#development-workflow)
- [Automation Overview](#automation-overview)
- [Troubleshooting CI](#troubleshooting-ci)
- [Project Structure](#project-structure)
- [Roadmap & Issues](#roadmap--issues)
- [License](#license)

## Features
### OpenAI Model Usage
- Defaults to the `o3` model. Parameters for this model are in `DEFAULT_O3_PARAMS`.
- Model and parameters can be overridden when calling `query_chatgpt()`.

### Web Search
- Integrates Google Custom Search (`web_search` tool).
- Triggered automatically when ChatGPT requests it.
- Replies include a `Sources:` section listing URLs.

### Discord Interaction
- Use the `/chat` slash command in servers, DMs and group DMs.
- Configure models and parameters with the `/manage` command group.
- Enable the bot in personal DMs by authorizing the App via the OAuth2 URL from the Discord developer portal.

### Message Handling
- Messages are split into 2 000‑character chunks.
- URLs are never cut in half.

## Getting Started
### Local Python
```bash
git clone <repo-url>
cd discord-lm-app
pip install -r requirements.txt
pip install -e .[dev]
pre-commit install
cp .env.example .env
python bot.py
```

### Docker
```bash
docker compose up --build -d
```
Check logs with `docker compose logs -f bot`.

### GitHub Codespaces
Create a codespace from the repo and then:
```bash
cp .env.example .env
python bot.py
```

## Configuration
All settings are provided through environment variables. Copy `.env.example` to `.env` and fill in:

| Variable | Purpose |
|----------|---------|
| `DISCORD_TOKEN` | Discord bot token |
| `OPENAI_API_KEY` | OpenAI API key |
| `GOOGLE_API_KEY` | Google API key |
| `GOOGLE_CSE_ID` | Google Custom Search Engine ID |

## Development Workflow
1. Fork and clone the repository.
2. Create a branch named `feature/<id>-short-description` or `fix/<id>-short-description`.
3. Install dependencies as in [Getting Started](#getting-started).
4. Run `pre-commit install` once, then rely on the commit hook or run `pre-commit run --all-files` manually.
5. Run formatting, linting, types and tests:
   ```bash
   black .
   ruff check . --fix
   mypy .
   pytest -q --cov
   ```
6. Use Conventional Commit messages (`feat:`, `fix:`…). Include the Task ID in the PR title.
7. Open a pull request. CI must pass all jobs (lint, types, tests, coverage, Docker build, docs build).

## Automation Overview
Several GitHub Actions keep the project healthy. See [docs/automation.md](docs/automation.md) for full details.
Briefly:
- **CI** – runs tests, lints, type checks, builds Docker image and docs, uploads coverage.
- **Release** – bumps version with semantic-release and publishes the Docker image.
- **Roadmap Sync** – updates `PROJECT_STATE.md` when issues change.
- **Issue Sync** – labels issues when related PRs merge.

## Troubleshooting CI
- **mypy fails** – ensure types are correct and modules are imported properly.
- **pytest fails** – run tests locally with `pytest -q` and fix failures.
- **docs-build fails** – run `mkdocs build --strict` and check broken links.

## Project Structure
- `src/discord_lm_bot/` – bot modules (`discord_bot.py`, `openai_client.py`, `search_tool.py`, `splitter.py`).
- `bot.py` – entry point that calls `discord_lm_bot.run_bot()`.
- `tools/` – helper scripts used by automation.

## Roadmap & Issues
See [PROJECT_STATE.md](PROJECT_STATE.md) for the current roadmap and open [GitHub Issues](https://github.com/flimedime0/discord-lm-app/issues) to report bugs or request features.

## License
MIT License. See [LICENSE](LICENSE) for details.
