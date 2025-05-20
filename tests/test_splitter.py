import pytest

from discord_lm_bot.discord_bot import send_slow_message


class DummyMessage:
    def __init__(self):
        self.edits = []

    async def edit(self, *, content=None):
        self.edits.append(content)
        return self


class DummyChannel:
    def __init__(self):
        self.sent = []

    async def send(self, text):
        msg = DummyMessage()
        self.sent.append(msg)
        return msg

    def typing(self):
        class _CM:
            async def __aenter__(self_inner):
                return None

            async def __aexit__(self_inner, exc_type, exc, tb):
                return False

        return _CM()


@pytest.mark.asyncio
async def test_url_never_split():
    prefix = "a" * 1995
    url = "https://example.com/very-long-url"
    suffix = "b" * (2100 - len(prefix) - len(url))
    text = prefix + url + suffix

    channel = DummyChannel()
    await send_slow_message(channel, text, delay=0)

    assert len(channel.sent) == 2
    first_final = channel.sent[0].edits[-1]
    second_first = channel.sent[1].edits[0]
    assert "http" not in first_final
    assert second_first.startswith("http")


@pytest.mark.asyncio
async def test_double_period_logic():
    trail = "Blah blah. 4."
    prefix = "a" * (1999 - trail.index("4"))
    text = prefix + trail

    channel = DummyChannel()
    await send_slow_message(channel, text, delay=0)

    assert len(channel.sent) == 2
    first_final = channel.sent[0].edits[-1]
    second_first = channel.sent[1].edits[0]
    assert first_final.endswith("blah.")
    assert second_first.startswith("4.")
