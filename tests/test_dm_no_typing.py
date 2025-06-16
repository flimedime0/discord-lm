# File purpose: Test DM replies succeed when typing indicator raises Forbidden.
from types import SimpleNamespace

import pytest

from discord_lm_bot import discord_bot


class DummyChannel:
    def __init__(self):
        self.messages: list[str] = []

    class DummyResp:
        status = 403
        reason = "Forbidden"

    def typing(self):
        raise discord_bot.discord.Forbidden(self.DummyResp(), "Missing Access")

    async def send(self, content):
        self.messages.append(content)


class DummyMessage:
    def __init__(self):
        self.author = SimpleNamespace(id=1, mention="@1")
        self.channel = DummyChannel()
        self.content = "hi"
        self.attachments = []


@pytest.mark.asyncio
async def test_dm_no_typing(monkeypatch):
    async def fake_reply(**kwargs):
        return "ok", False, "gpt-4o"

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)
    monkeypatch.setattr(discord_bot.discord, "DMChannel", DummyChannel)

    msg = DummyMessage()
    await discord_bot.on_message(msg)

    assert msg.channel.messages == ["ok – @1"]
