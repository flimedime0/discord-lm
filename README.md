# Discord LM App

This repository contains a minimal Discord bot powered by `discord.py`.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Discord bot token in the `DISCORD_TOKEN` environment variable.

3. Run the bot:
   ```bash
   python -m bot.main
   ```

The bot provides a single `!echo` command that repeats whatever message you pass to it.

## Testing

Run the unit tests with:

```bash
pytest
```
