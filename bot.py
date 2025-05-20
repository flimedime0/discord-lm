import discord
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_oai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def send_slow_message(channel, text, chunk=32, delay=1.0):
    """
    Reveals text in 32-character chunks every second.
    1 edit/sec respects Discord’s rate limit.
    """
    sent = await channel.send("…")        # non-empty placeholder
    displayed = ""
    async with channel.typing():
        for i, ch in enumerate(text, start=1):
            displayed += ch
            if i % chunk == 0 or i == len(text):
                await sent.edit(content=displayed)
                await asyncio.sleep(delay)
    return sent

async def query_chatgpt(prompt: str) -> str:
    response = await client_oai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        top_p=0,
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
