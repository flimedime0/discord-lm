import pytest

from discord_lm_bot import discord_bot


class DummyUser:
    id = 1


class DummyMessage:
    def __init__(self, author):
        self.author = author
        self.mentions = []
        self.content = ""
        self.channel = None


class DummyClient:
    def __init__(self, user):
        self.user = user


@pytest.mark.asyncio
async def test_on_message_ignores_self(monkeypatch):
    dummy = DummyUser()
    monkeypatch.setattr(discord_bot, "client", DummyClient(dummy))
    msg = DummyMessage(dummy)
    await discord_bot.on_message(msg)
