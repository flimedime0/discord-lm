import asyncio
import json
import re

import discord
from discord import app_commands
import traceback

from .config import DISCORD_TOKEN, OPENAI_API_KEY
from .openai_client import call_chat, DEFAULT_O3_PARAMS, SYSTEM_CITE
from .search_tool import SEARCH_TOOL, do_search
from .splitter import split_message

URL_RE = re.compile(r"https?://\S+")

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def send_slow_message(channel, text, chunk=192, delay=1.0, max_len=2000):
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
                    split_at = max_len - 1

                    # walk backward for the last URL before the split point
                    last_url = None
                    for m in URL_RE.finditer(displayed, 0, split_at + 1):
                        last_url = m

                    if last_url and last_url.end() > split_at:
                        split_at = max(0, last_url.start() - 1)

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
                        break  # no leftover text → exit loop
                else:
                    await sent.edit(content=displayed)
                await asyncio.sleep(delay)
    return sent


async def query_chatgpt(prompt: str, model: str = "o3", **overrides) -> str:
    merged = DEFAULT_O3_PARAMS.copy()
    merged.update(overrides)
    params = {k: v for k, v in merged.items() if v is not None}

    # 1st request – let the model decide if it needs search unless forced
    r1 = await call_chat(
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
        history.extend(
            [
                {"role": "user", "content": prompt},
                msg,  # assistant message containing tool_calls
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": "web_search",
                    "content": result_json,
                },
            ]
        )

        r2 = await call_chat(
            model=model,
            messages=history,
            **params,
        )
        return r2.choices[0].message.content

    # No search needed
    return msg.content


@tree.command(name="chat", description="Send a prompt to the AI model in servers or DMs.")
@app_commands.describe(prompt="The prompt or question for the AI.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def slash_chat(interaction: discord.Interaction, prompt: str):
    """Handles the /chat slash command."""
    try:
        await interaction.response.defer(thinking=True, ephemeral=False)

        model_to_use = "o3"
        params_to_use = DEFAULT_O3_PARAMS.copy()

        reply_text = await query_chatgpt(
            prompt=prompt,
            model=model_to_use,
            history=None,
            **params_to_use,
        )

        if len(reply_text) <= 2000:
            await interaction.followup.send(reply_text)
        else:
            chunks = split_message(reply_text, 1950)
            for i, chunk_text in enumerate(chunks):
                if i == 0:
                    await interaction.followup.send(chunk_text)
                else:
                    if isinstance(interaction.channel, discord.abc.Messageable):
                        await interaction.channel.send(chunk_text)

    except Exception as e:
        error_message = f"Sorry, I encountered an error: {type(e).__name__}"
        channel_id = getattr(interaction.channel, "id", "unknown")
        print(f"Error in /chat command for user {interaction.user.id} in channel {channel_id}:")
        traceback.print_exc()
        if interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        await tree.sync()
        print(
            f"Slash commands synced globally: {[command.name for command in tree.get_commands()]}"
        )
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")
        traceback.print_exc()


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


def run_bot() -> None:
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        print("Environment variables DISCORD_TOKEN and OPENAI_API_KEY must be set.")
    else:
        client.run(DISCORD_TOKEN)
