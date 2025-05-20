import discord
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_oai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_O3_PARAMS = {
    "temperature": 1,
    # optional tuning knobs you may want:
    "max_tokens": None,
    "stop": None,
    "seed": None,
    # "stream": False,
}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def send_slow_message(channel, text,
                             chunk=192, delay=1.0, max_len=2000):
    """Reveals `text` in 192-char chunks every second.
    When content > max_len, closes sentence at last period and continues in a
    new Discord message."""
    sent = await channel.send("…")
    displayed = ""
    async with channel.typing():
        for i, ch in enumerate(text, start=1):
            displayed += ch
            hit_chunk = (i % chunk == 0) or (i == len(text))
            if hit_chunk:
                if len(displayed) > max_len:
                    split_at = displayed.rfind(".", 0, max_len)
                    if split_at == -1:
                        split_at = max_len - 1
                    segment = displayed[: split_at + 1]
                    remainder = displayed[split_at + 1 :]
                    await sent.edit(content=segment.strip())
                    sent = await channel.send("…")
                    displayed = remainder.lstrip()
                else:
                    await sent.edit(content=displayed)
                await asyncio.sleep(delay)
    return sent

async def query_chatgpt(prompt: str,
                        model: str = "o3",
                        **overrides) -> str:
    params = DEFAULT_O3_PARAMS.copy()
    params.update(overrides)
    params = {k: v for k, v in params.items() if v is not None}

    response = await client_oai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        **params,
    )
    return response.choices[0].message.content

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith('!ask'):
        user_prompt = message.content[len('!ask '):]
        try:
            async with message.channel.typing():
                reply = await query_chatgpt(user_prompt)
            await send_slow_message(message.channel, reply)
        except Exception as e:
            await message.channel.send('Error querying ChatGPT')
            print(e)

if __name__ == '__main__':
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        print('Environment variables DISCORD_TOKEN and OPENAI_API_KEY must be set')
    else:
        client.run(DISCORD_TOKEN)
