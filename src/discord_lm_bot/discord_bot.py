import json
import re

import discord
from discord import app_commands
import traceback

from .config import DISCORD_TOKEN, OPENAI_API_KEY
from .database import get_user_settings, set_user_setting, setup_database
from .llm_config import GLOBAL_DEFAULTS
from .openai_client import call_chat
from .search_tool import SEARCH_TOOL, do_search
from .splitter import split_message

URL_RE = re.compile(r"https?://\S+")

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

_active_queries: set[int] = set()


async def query_chatgpt(
    *, prompt: str, user_id: int, image_urls: list[str] | None = None
) -> tuple[str, bool, str]:
    settings = get_user_settings(user_id) or GLOBAL_DEFAULTS
    model = settings.get("active_model") or GLOBAL_DEFAULTS["model"]

    # 1st request – let the model decide if it needs search unless forced
    content: list[dict] = [{"type": "text", "text": prompt}]
    for url in image_urls or []:
        content.append({"type": "image_url", "image_url": {"url": url}})

    r1 = await call_chat(
        model=model,
        messages=[{"role": "user", "content": content}],
        tools=[SEARCH_TOOL],
        tool_choice="auto",
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

        history = [
            {"role": "user", "content": content},
            msg,
            {
                "role": "tool",
                "tool_call_id": call.id,
                "name": "web_search",
                "content": result_json,
            },
        ]

        r2 = await call_chat(
            model=model,
            messages=history,
        )
        return r2.choices[0].message.content, True, model

    # No search needed
    return msg.content, False, model


@tree.command(name="chat", description="Send a prompt to the AI model in servers or DMs.")
@app_commands.describe(prompt="The prompt or question for the AI.")
@app_commands.describe(model="Optional model override")
@app_commands.choices(
    model=[
        app_commands.Choice(name="gpt-4o", value="gpt-4o"),
        app_commands.Choice(name="o3", value="o3"),
    ]
)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def slash_chat(
    interaction: discord.Interaction,
    *,
    prompt: str,
    model: app_commands.Choice[str] | None = None,
):
    """Handles the /chat slash command."""
    try:
        if interaction.user.id in _active_queries:
            await interaction.response.send_message(
                "Please wait for my current reply to finish.",
                ephemeral=True,
            )
            return
        _active_queries.add(interaction.user.id)
        all_attachments = getattr(interaction, "attachments", [])
        images = [
            a for a in all_attachments if a.content_type and a.content_type.startswith("image/")
        ][:10]
        await interaction.response.defer(thinking=False, ephemeral=False)

        if len(all_attachments) > 10:
            await interaction.followup.send(
                "Only the first 10 images were processed; the rest were ignored.",
                ephemeral=True,
            )

        if model is not None:
            set_user_setting(interaction.user.id, "active_model", model.value)

        if isinstance(interaction.channel, discord.DMChannel):
            async with interaction.channel.typing():
                reply_text, search_used, model_used = await query_chatgpt(
                    prompt=prompt,
                    user_id=interaction.user.id,
                    image_urls=[img.url for img in images],
                )
        else:
            reply_text, search_used, model_used = await query_chatgpt(
                prompt=prompt,
                user_id=interaction.user.id,
                image_urls=[img.url for img in images],
            )

        suffix = f" – {interaction.user.mention}"
        search_notice = "\n\nWeb search was used to answer your question." if search_used else ""
        footer = f"\n\nModel used: {model_used}"

        chunks = split_message(reply_text + search_notice + footer, suffix_len=len(suffix))
        for chunk in chunks:
            await interaction.followup.send(chunk + suffix)

    except Exception as e:
        error_message = f"Sorry, I encountered an error: {type(e).__name__}"
        channel_id = getattr(interaction.channel, "id", "unknown")
        print(f"Error in /chat command for user {interaction.user.id} in channel {channel_id}:")
        traceback.print_exc()
        if interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)
    finally:
        _active_queries.discard(interaction.user.id)


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


def run_bot() -> None:
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        print("Environment variables DISCORD_TOKEN and OPENAI_API_KEY must be set.")
    else:
        setup_database()
        client.run(DISCORD_TOKEN)
