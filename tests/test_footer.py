# File purpose: Test message footer and mention handling.
from types import SimpleNamespace

import pytest

from discord_lm_bot import discord_bot


class DummyResponse:
    def __init__(self):
        self.sent = None
        self.deferred = False

    async def send_message(self, content, ephemeral=False):
        self.sent = content

    async def defer(self, thinking=False, ephemeral=False):
        self.deferred = True

    def is_done(self):
        return self.deferred


class DummyFollowup:
    def __init__(self):
        self.messages = []

    async def send(self, content):
        self.messages.append(content)


class DummyInteraction:
    def __init__(self, user_id):
        self.user = SimpleNamespace(id=user_id, mention=f"@{user_id}")
        self.response = DummyResponse()
        self.followup = DummyFollowup()
        self.channel = SimpleNamespace(id=123)
        self.attachments = []


@pytest.mark.asyncio
async def test_footer_and_mentions(monkeypatch):
    async def fake_reply(**kwargs):
        return "x" * 2100, False, "gpt-4o"

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)

    i = DummyInteraction(1)
    await discord_bot.slash_chat.callback(i, prompt="hi")

    assert len(i.followup.messages) == 2
    assert all(m.endswith(" – @1") for m in i.followup.messages)
    assert "Model used: gpt-4o" in i.followup.messages[-1]
