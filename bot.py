import discord
import openai
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

client = discord.Client(intents=discord.Intents.default())

async def query_chatgpt(prompt: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message['content']

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
            reply = await query_chatgpt(user_prompt)
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send('Error querying ChatGPT')
            print(e)

if __name__ == '__main__':
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        print('Environment variables DISCORD_TOKEN and OPENAI_API_KEY must be set')
    else:
        client.run(DISCORD_TOKEN)
