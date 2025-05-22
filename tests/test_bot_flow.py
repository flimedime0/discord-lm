import asyncio
from contextlib import asynccontextmanager

import pytest

from discord_lm_bot.discord_bot import send_slow_message


class FakeMessage:
    def __init__(self, content=""):
        self.content = content

    async def edit(self, content=None):
        if content is not None:
            self.content = content
        return self


class FakeChannel:
    def __init__(self):
        self.sent = []

    async def send(self, content):
        msg = FakeMessage(content)
        self.sent.append(msg)
        return msg

    @asynccontextmanager
    async def typing(self):
        yield


@pytest.mark.asyncio
async def test_send_slow_message_chunks(monkeypatch):
    channel = FakeChannel()

    async def dummy_sleep(*_):
        return None

    monkeypatch.setattr(asyncio, "sleep", dummy_sleep)
    text = "a" * 2100
    await send_slow_message(channel, text, chunk=2100, delay=0, max_len=2000)
    assert len(channel.sent) == 2
    assert channel.sent[0].content == "a" * 2000
