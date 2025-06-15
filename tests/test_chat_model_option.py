import pytest
from types import SimpleNamespace

from discord_lm_bot import discord_bot


class DummyResponse:
    def __init__(self):
        self.deferred = False

    async def send_message(self, *_args, **_kwargs):
        pass

    async def defer(self, *args, **kwargs):
        self.deferred = True

    def is_done(self):
        return self.deferred


class DummyFollowup:
    async def send(self, *args, **kwargs):
        pass


class DummyInteraction:
    def __init__(self):
        self.user = SimpleNamespace(id=1, mention="@1")
        self.response = DummyResponse()
        self.followup = DummyFollowup()
        self.channel = SimpleNamespace(id=123)
        self.attachments = []


@pytest.mark.asyncio
async def test_model_option_updates_db(monkeypatch):
    recorded = {}

    async def fake_reply(**kwargs):
        return "ok", False

    def fake_set(user_id, key, value):
        recorded["user_id"] = user_id
        recorded["key"] = key
        recorded["value"] = value

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)
    monkeypatch.setattr(discord_bot, "set_user_setting", fake_set)

    i = DummyInteraction()
    await discord_bot.slash_chat.callback(
        i, prompt="hi", model=discord_bot.app_commands.Choice(name="gpt-4o", value="gpt-4o")
    )

    assert recorded == {"user_id": 1, "key": "active_model", "value": "gpt-4o"}
