# File purpose: Test plain DM replies include mentions on every chunk.
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest

from discord_lm_bot import discord_bot


class DummyChannel:
    def __init__(self):
        self.messages: list[str] = []
        self.typing_called = False

    @asynccontextmanager
    async def typing(self):
        self.typing_called = True
        yield

    async def send(self, content):
        self.messages.append(content)


class DummyMessage:
    def __init__(self):
        self.author = SimpleNamespace(id=1, mention="@1")
        self.channel = DummyChannel()
        self.content = "hi"
        self.attachments = []


@pytest.mark.asyncio
async def test_dm_suffix(monkeypatch):
    async def fake_reply(**kwargs):
        return "x" * 2100, False, "gpt-4o"

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)
    monkeypatch.setattr(discord_bot.discord, "DMChannel", DummyChannel)

    msg = DummyMessage()
    await discord_bot.on_message(msg)

    assert msg.channel.typing_called
    assert len(msg.channel.messages) == 2
    assert all(m.endswith(" – @1") for m in msg.channel.messages)
