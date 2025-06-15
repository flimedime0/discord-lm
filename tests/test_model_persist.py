import types
import pytest

from discord_lm_bot import discord_bot, database


class DummyResponse:
    def __init__(self):
        self.deferred = False

    async def send_message(self, content, ephemeral=False):
        self.sent = (content, ephemeral)

    async def defer(self, thinking=False, ephemeral=False):
        self.deferred = True

    def is_done(self):
        return self.deferred


class DummyFollowup:
    def __init__(self):
        self.messages = []

    async def send(self, content, ephemeral=False):
        self.messages.append((content, ephemeral))


class DummyInteraction:
    def __init__(self, user_id):
        self.user = types.SimpleNamespace(id=user_id, mention=f"@{user_id}")
        self.response = DummyResponse()
        self.followup = DummyFollowup()
        self.channel = types.SimpleNamespace(id=123)
        self.attachments = []


@pytest.mark.asyncio
async def test_model_arg_persists(tmp_path, monkeypatch):
    db_file = tmp_path / "db.sqlite3"
    monkeypatch.setattr(database, "DB_PATH", db_file)
    database.setup_database()

    recorded = []

    async def fake_reply(**kwargs):
        settings = database.get_user_settings(kwargs["user_id"])
        recorded.append(settings["active_model"])
        return "ok", False, "gpt-4o"

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)

    i = DummyInteraction(1)
    choice = types.SimpleNamespace(value="o3")
    await discord_bot.slash_chat.callback(i, prompt="hi", model=choice)
    await discord_bot.slash_chat.callback(i, prompt="hi", model=None)

    assert recorded[-1] == "o3"
