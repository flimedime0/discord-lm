import json

import pytest

from bot import do_search

@pytest.mark.asyncio
async def test_do_search_no_keys(monkeypatch):
    monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
    monkeypatch.delenv('GOOGLE_CSE_ID', raising=False)
    result = await do_search('python')
    data = json.loads(result)
    assert data == [{"error": "Google CSE keys not set"}]
