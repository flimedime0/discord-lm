import asyncio
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


@pytest.mark.asyncio
async def test_concurrency_lock(monkeypatch):
    async def slow_reply(**kwargs):
        await asyncio.sleep(0.1)
        return "ok", False

    monkeypatch.setattr(discord_bot, "query_chatgpt", slow_reply)

    i1 = DummyInteraction(1)
    i2 = DummyInteraction(1)

    task1 = asyncio.create_task(discord_bot.slash_chat.callback(i1, prompt="hi"))
    await asyncio.sleep(0)  # let task1 start and add to lock
    await discord_bot.slash_chat.callback(i2, prompt="hi")

    await task1

    assert i2.response.sent.startswith("\U0001f6a7")
