# File purpose: Test /chat behavior in DMs using slash commands.
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest

from discord_lm_bot import discord_bot


class DummyChannel:
    def __init__(self):
        self.typing_called = False

    @asynccontextmanager
    async def typing(self):
        self.typing_called = True
        yield


class DummyResponse:
    def __init__(self):
        self.deferred = False

    async def defer(self, thinking=False, ephemeral=False):
        self.deferred = True

    async def send_message(self, content, ephemeral=False):
        pass

    def is_done(self):
        return self.deferred


class DummyFollowup:
    def __init__(self):
        self.messages = []

    async def send(self, content):
        self.messages.append(content)


class DummyInteraction:
    def __init__(self):
        self.user = SimpleNamespace(id=1, mention="@1")
        self.channel = DummyChannel()
        self.response = DummyResponse()
        self.followup = DummyFollowup()
        self.attachments = []


@pytest.mark.asyncio
async def test_dm_slash(monkeypatch):
    async def fake_reply(**kwargs):
        return "ok", False, "gpt-4o"

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)
    monkeypatch.setattr(discord_bot.discord, "DMChannel", DummyChannel)

    interaction = DummyInteraction()
    await discord_bot.slash_chat.callback(interaction, prompt="hi")

    assert interaction.response.deferred
    assert interaction.channel.typing_called
    assert interaction.followup.messages
