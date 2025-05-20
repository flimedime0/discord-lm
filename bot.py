import discord
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
import httpx
import json

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

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the public internet for up-to-date information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query",
                },
                "num_results": {
                    "type": "integer",
                    "description": "How many results (1-10)",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
}

async def do_search(query: str, num_results: int = 5) -> str:
    """Return a short JSON string of search results from DuckDuckGo."""
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_redirect": 1}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, timeout=10)
        data = r.json()
    related = data.get("RelatedTopics", [])[:num_results]
    snippets = [
        {"title": t.get("Text", ""), "url": t.get("FirstURL", "")}
        for t in related if "Text" in t
    ]
    return json.dumps(snippets, ensure_ascii=False)

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
    params = {k: v for k, v in (DEFAULT_O3_PARAMS | overrides).items()
              if v is not None}

    # 1st request – let the model decide if it needs search
    r1 = await client_oai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        tools=[SEARCH_TOOL],
        tool_choice="auto",
        **params,
    )
    msg = r1.choices[0].message

    # msg is the assistant message that requested the tool
    if msg.tool_calls:
        call = msg.tool_calls[0]
        args = json.loads(call.function.arguments)
        result_json = await do_search(
            args["query"],
            args.get("num_results", 5)
        )

        # Build conversation so far
        history = [
            {"role": "user", "content": prompt},
            msg,
            {
                "role": "tool",
                "tool_call_id": call.id,
                "name": "web_search",
                "content": result_json,
            },
        ]

        r2 = await client_oai.chat.completions.create(
            model=model,
            messages=history,
            **params,
        )
        return r2.choices[0].message.content

    # No search needed
    return msg.content

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message: discord.Message):
    # ignore messages from ourselves
    if message.author == client.user:
        return

    # respond only if the bot is mentioned
    if client.user in message.mentions:
        # strip the mention text from the prompt
        prompt = message.content
        for mention in message.mentions:
            if mention == client.user:
                prompt = prompt.replace(f"<@{mention.id}>", "").strip()

        if not prompt:
            await message.channel.send("Ask me something after the mention.")
            return

        try:
            async with message.channel.typing():
                reply = await query_chatgpt(prompt)
            await send_slow_message(message.channel, reply)
        except Exception as e:
            await message.channel.send("Error querying ChatGPT.")
            print(e)

    # else: ignore message (no command prefix needed)

if __name__ == '__main__':
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        print('Environment variables DISCORD_TOKEN and OPENAI_API_KEY must be set.')
    else:
        client.run(DISCORD_TOKEN)
