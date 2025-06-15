import types
from contextlib import asynccontextmanager

import pytest

from discord_lm_bot import discord_bot


class DummyChannel:
    def __init__(self):
        self.typing_called = False
        self.messages = []

    @asynccontextmanager
    async def typing(self):
        self.typing_called = True
        yield

    async def send(self, content):
        self.messages.append(content)


@pytest.mark.asyncio
async def test_dm_typing(monkeypatch):
    async def fake_reply(**kwargs):
        return "ok", False

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)

    channel = DummyChannel()
    monkeypatch.setattr(discord_bot.discord, "DMChannel", DummyChannel)
    msg = types.SimpleNamespace(
        author=types.SimpleNamespace(id=1, mention="@1"),
        content="hi",
        channel=channel,
        attachments=[],
    )
    await discord_bot.on_message(msg)

    assert channel.typing_called
