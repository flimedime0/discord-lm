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

async def send_slow_message(channel: discord.abc.Messageable, text: str, delay: float = 0.05):
    """Send a message with a typing effect by editing it character by character."""
    sent_message = await channel.send("…")
    displayed = ""
    async with channel.typing():
        for ch in text:
            displayed += ch
            await sent_message.edit(content=displayed)
            await asyncio.sleep(delay)
    return sent_message

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
