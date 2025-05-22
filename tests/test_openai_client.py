from unittest import mock

import pytest

from discord_lm_bot import openai_client


@pytest.mark.asyncio
async def test_call_chat_retries(monkeypatch):
    calls = 0

    async def fake_create(**kwargs):
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError("fail")
        return mock.Mock()

    client = mock.Mock()
    client.chat.completions.create = fake_create

    monkeypatch.setattr(openai_client, "client_oai", lambda: client)

    async def no_sleep(*_):
        return None

    openai_client.call_chat.retry.sleep = no_sleep

    await openai_client.call_chat(model="gpt")
    assert calls == 3
