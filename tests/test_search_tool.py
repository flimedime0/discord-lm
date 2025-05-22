import json
import os
from unittest import mock

import pytest

from discord_lm_bot import search_tool


@pytest.mark.asyncio
async def test_do_search_parses_json(monkeypatch):
    async def fake_get(url, params=None, timeout=None):
        class Resp:
            def json(self):
                return {"items": [{"title": "t", "link": "u", "snippet": "s"}]}

        return Resp()

    client = mock.AsyncMock()
    client.__aenter__.return_value = client
    client.get.side_effect = fake_get

    monkeypatch.setattr("httpx.AsyncClient", lambda: client)
    monkeypatch.setitem(os.environ, "GOOGLE_API_KEY", "x")
    monkeypatch.setitem(os.environ, "GOOGLE_CSE_ID", "y")

    async def no_sleep(*_):
        return None

    search_tool.retry_oai.sleep = no_sleep

    data = await search_tool.do_search("hi", 1)
    assert json.loads(data)[0]["url"] == "u"
