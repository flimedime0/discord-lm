import json
import re
import sqlite3

import discord
from discord import app_commands
import traceback

from .config import DISCORD_TOKEN, OPENAI_API_KEY
from .database import DB_PATH, get_user_settings, set_user_setting, setup_database
from .llm_config import GLOBAL_DEFAULTS, SUPPORTED_PARAMS
from .openai_client import call_chat
from .search_tool import SEARCH_TOOL, do_search
from .splitter import split_message

URL_RE = re.compile(r"https?://\S+")

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def query_chatgpt(*, prompt: str, user_id: int) -> tuple[str, bool]:
    settings = get_user_settings(user_id) or GLOBAL_DEFAULTS
    model = settings.get("active_model") or GLOBAL_DEFAULTS["model"]
    params = GLOBAL_DEFAULTS["params"].copy()
    params.update(settings.get("params", {}))

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

        r2 = await call_chat(
            model=model,
            messages=history,
            **params,
        )
        return r2.choices[0].message.content, True

    # No search needed
    return msg.content, False


@tree.command(name="chat", description="Send a prompt to the AI model in servers or DMs.")
@app_commands.describe(prompt="The prompt or question for the AI.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def slash_chat(interaction: discord.Interaction, prompt: str):
    """Handles the /chat slash command."""
    try:
        await interaction.response.defer(thinking=False, ephemeral=False)

        reply_text, search_used = await query_chatgpt(
            prompt=prompt,
            user_id=interaction.user.id,
        )

        final_reply = f"{interaction.user.mention} {reply_text}"
        if search_used:
            final_reply += "\n\n---\n*🔍 Web search used for this response.*"

        chunks = split_message(final_reply)
        for chunk in chunks:
            await interaction.followup.send(chunk)

    except Exception as e:
        error_message = f"Sorry, I encountered an error: {type(e).__name__}"
        channel_id = getattr(interaction.channel, "id", "unknown")
        print(f"Error in /chat command for user {interaction.user.id} in channel {channel_id}:")
        traceback.print_exc()
        if interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)


manage = app_commands.Group(name="manage", description="Manage your bot settings")


@manage.command(name="view", description="View your current settings")
async def manage_view(interaction: discord.Interaction):
    settings = get_user_settings(interaction.user.id) or GLOBAL_DEFAULTS
    await interaction.response.send_message(str(settings), ephemeral=True)


@manage.command(name="use_model", description="Choose your active model")
@app_commands.describe(model="Model to use")
@app_commands.choices(
    model=[
        app_commands.Choice(name="gpt-4o", value="gpt-4o"),
        app_commands.Choice(name="o3", value="o3"),
    ]
)
async def manage_use_model(interaction: discord.Interaction, model: app_commands.Choice[str]):
    set_user_setting(interaction.user.id, "active_model", model.value)
    await interaction.response.send_message(f"Model set to {model.value}", ephemeral=True)


@manage.command(name="tune_parameter", description="Set a parameter for the current model")
@app_commands.describe(name="Parameter name", value="Value for the parameter")
@app_commands.choices(
    name=[
        app_commands.Choice(name="temperature", value="temperature"),
        app_commands.Choice(name="top_p", value="top_p"),
        app_commands.Choice(name="max_tokens", value="max_tokens"),
    ]
)
async def manage_tune_parameter(
    interaction: discord.Interaction, name: app_commands.Choice[str], value: str
):
    settings = get_user_settings(interaction.user.id) or GLOBAL_DEFAULTS
    model = settings.get("active_model") or GLOBAL_DEFAULTS["model"]
    if name.value not in SUPPORTED_PARAMS.get(model, []):
        await interaction.response.send_message(
            "Parameter not supported for this model", ephemeral=True
        )
        return
    try:
        if name.value in {"temperature", "top_p"}:
            val = float(value)
        else:
            val = int(value)
    except ValueError:
        await interaction.response.send_message("Invalid value", ephemeral=True)
        return
    if name.value == "temperature" and not (0 <= val <= 2):
        await interaction.response.send_message("temperature must be 0-2", ephemeral=True)
        return
    if name.value == "top_p" and not (0 <= val <= 1):
        await interaction.response.send_message("top_p must be 0-1", ephemeral=True)
        return
    set_user_setting(interaction.user.id, name.value, val)
    await interaction.response.send_message(f"{name.value} set to {val}", ephemeral=True)


@manage.command(name="reset_all", description="Reset all settings")
async def manage_reset(interaction: discord.Interaction):
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute("DELETE FROM user_preferences WHERE user_id=?", (interaction.user.id,))
    conn.close()
    await interaction.response.send_message("Settings reset", ephemeral=True)


tree.add_command(manage)


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


def run_bot() -> None:
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        print("Environment variables DISCORD_TOKEN and OPENAI_API_KEY must be set.")
    else:
        setup_database()
        client.run(DISCORD_TOKEN)
