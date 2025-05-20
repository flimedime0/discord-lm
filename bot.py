import discord
from discord import app_commands
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
import httpx
import json
import re
import traceback

URL_RE = re.compile(r"https?://\S+")
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_oai = AsyncOpenAI(api_key=OPENAI_API_KEY)

DEFAULT_PARAMS = {
    "temperature": float(os.getenv("OAI_TEMPERATURE", "1")),
    "top_p": float(os.getenv("OAI_TOP_P", "1")),
    "max_tokens": (
        int(os.getenv("OAI_MAX_TOKENS"))
        if os.getenv("OAI_MAX_TOKENS")
        else None
    ),
    "stop": os.getenv("OAI_STOP"),
    "seed": (
        int(os.getenv("OAI_SEED")) if os.getenv("OAI_SEED") else None
    ),
    # "stream": False,
}

MODEL_SETTINGS = {
    "o3": DEFAULT_PARAMS.copy(),
    "4o": DEFAULT_PARAMS.copy(),
}

CURRENT_MODEL = os.getenv("OAI_MODEL", "o3")

# System prompt enforcing inline citations with a source list
SYSTEM_CITE = (
    "After answering, add a line 'Sources:' followed by every URL from "
    "web_search, one per line. Speak naturally."
)

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

async def do_search(query: str, num_results: int = 8) -> str:
    """Return Google CSE results (title + link) as JSON string."""

    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id  = os.getenv("GOOGLE_CSE_ID")
    if not api_key or not cse_id:
        return json.dumps([{"error": "Google CSE keys not set"}])

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx":  cse_id,
        "q":   query,
        "num": max(1, min(num_results, 10)),
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, timeout=10)
        data = r.json()

    items = data.get("items", [])
    results = [
        {"title": it["title"], "url": it["link"], "snippet": it["snippet"]}
        for it in items
    ]
    return json.dumps(results, ensure_ascii=False)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.tree.command(name="chat", description="Ask ChatGPT")
@app_commands.describe(prompt="Your question")
async def slash_chat(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    try:
        reply = await query_chatgpt(
            prompt,
            model=CURRENT_MODEL,
            **MODEL_SETTINGS[CURRENT_MODEL],
        )
        await send_slow_message(interaction.channel, reply)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)
        traceback.print_exc()


@client.tree.command(name="options", description="View or set model options")
@app_commands.describe(
    model="Model to configure (o3 or 4o)",
    temperature="Model temperature",
    top_p="Nucleus sampling top_p",
    max_tokens="Maximum tokens in reply",
)
async def slash_options(
    interaction: discord.Interaction,
    model: str | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    max_tokens: int | None = None,
):
    global CURRENT_MODEL
    target = model or CURRENT_MODEL
    if target not in MODEL_SETTINGS:
        await interaction.response.send_message(
            "Model must be 'o3' or '4o'",
            ephemeral=True,
        )
        return

    if model:
        CURRENT_MODEL = model

    opts = MODEL_SETTINGS[target]
    if temperature is not None:
        opts["temperature"] = temperature
    if top_p is not None:
        opts["top_p"] = top_p
    if max_tokens is not None:
        opts["max_tokens"] = max_tokens

    await interaction.response.send_message(
        f"Current model: {CURRENT_MODEL}\n"
        f"{target} options: temperature={opts['temperature']}, "
        f"top_p={opts['top_p']}, max_tokens={opts['max_tokens']}",
        ephemeral=True,
    )


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
                    # provisional cut at Discord’s hard cap
                    split_at = 1999

                    # walk backward for the last URL before the split point
                    last_url = None
                    for m in URL_RE.finditer(displayed, 0, split_at + 1):
                        last_url = m

                    if last_url and last_url.end() > split_at:
                        split_at = last_url.start() - 1

                    # if still mid-word, back up to previous space or period
                    if displayed[split_at].isalnum():
                        p_space = displayed.rfind(" ", 0, split_at)
                        p_dot = displayed.rfind(".", 0, split_at)
                        p = max(p_space, p_dot)
                        if p != -1:
                            split_at = p

                    segment = displayed[: split_at + 1]
                    remainder = displayed[split_at + 1 :]


                    await sent.edit(content=segment.strip())

                    # create new placeholder ONLY if there’s more text
                    if remainder.strip():
                        sent = await channel.send("…")
                        displayed = remainder.lstrip()
                    else:
                        break   # no leftover text → exit loop
                else:
                    await sent.edit(content=displayed)
                await asyncio.sleep(delay)
    return sent

async def query_chatgpt(prompt: str,
                        model: str = "o3",
                        **overrides) -> str:
    params = {k: v for k, v in (DEFAULT_PARAMS | overrides).items()
              if v is not None}

    # 1st request – let the model decide if it needs search unless forced
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
            args.get("num_results", 8),
        )

        # Build conversation so far with citation rules
        history = []
        if SYSTEM_CITE:
            history.append({"role": "system", "content": SYSTEM_CITE})
        history.extend([
            {"role": "user", "content": prompt},
            msg,  # assistant message containing tool_calls
            {
                "role": "tool",
                "tool_call_id": call.id,
                "name": "web_search",
                "content": result_json,
            },
        ])

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
    try:
        synced = await client.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

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
                reply = await query_chatgpt(
                    prompt,
                    model=CURRENT_MODEL,
                    **MODEL_SETTINGS[CURRENT_MODEL],
                )
            await send_slow_message(message.channel, reply)
        except Exception as e:
            await message.channel.send(f"Error: {e}")
            traceback.print_exc()

    # else: ignore message (no command prefix needed)

if __name__ == '__main__':
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        print('Environment variables DISCORD_TOKEN and OPENAI_API_KEY must be set.')
    else:
        if not os.getenv('GOOGLE_API_KEY') or not os.getenv('GOOGLE_CSE_ID'):
            print('Google search disabled (GOOGLE_API_KEY or GOOGLE_CSE_ID not set)')
        client.run(DISCORD_TOKEN)
