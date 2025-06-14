import pytest
from types import SimpleNamespace

from discord_lm_bot import discord_bot


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
    def __init__(self, attachments):
        self.user = SimpleNamespace(id=1, mention="@1")
        self.response = DummyResponse()
        self.followup = DummyFollowup()
        self.channel = SimpleNamespace(id=123)
        self.attachments = attachments


@pytest.mark.asyncio
async def test_attachment_limit(monkeypatch):
    recorded = {}

    async def fake_reply(**kwargs):
        recorded["urls"] = kwargs["image_urls"]
        return "ok", False

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)

    attachments = [
        SimpleNamespace(url=f"http://img{i}", content_type="image/png") for i in range(12)
    ]
    i = DummyInteraction(attachments)

    await discord_bot.slash_chat.callback(i, prompt="hi")

    assert len(recorded["urls"]) == 10
    assert i.followup.messages[0][1] is True
    assert "Only the first 10 images" in i.followup.messages[0][0]


@pytest.mark.asyncio
async def test_attachment_pass_through(monkeypatch):
    recorded = {}

    async def fake_reply(**kwargs):
        recorded["urls"] = kwargs["image_urls"]
        return "ok", False

    monkeypatch.setattr(discord_bot, "query_chatgpt", fake_reply)

    attachments = [
        SimpleNamespace(url="http://img.png", content_type="image/png") for _ in range(3)
    ]
    i = DummyInteraction(attachments)

    await discord_bot.slash_chat.callback(i, prompt="hi")

    assert len(recorded["urls"]) == 3
    assert not any(e for _msg, e in i.followup.messages)
