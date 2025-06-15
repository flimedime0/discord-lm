# Usage

## Running with Python

1. Install dependencies with `pip install -r requirements.txt`.
2. Configure your `.env` file.
3. Start the bot with `python bot.py`.

## Running with Docker

```bash
docker compose up --build -d
```

## Interacting with the Bot

- Use the `/chat` slash command to send prompts. It works in servers, DMs and group DMs.
- You can attach up to 10 images to `/chat` for multimodal prompts. You may also specify `model=gpt-4o` or `model=o3` to persist your choice.
- Replies mention you at the end of each message.
- Authorize the App using your OAuth2 URL to enable DM or group DM usage.
