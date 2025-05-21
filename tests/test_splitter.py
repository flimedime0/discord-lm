from discord_lm_bot.splitter import split_message


def test_split_message_no_url_split():
    base = "x" * 1995
    url = " https://example.com/test"
    segments = split_message(base + url)
    assert len(segments) == 2
    assert segments[0] == base
    assert segments[1] == url.strip()


def test_split_message_no_blank_segment():
    text = "a" * 1999 + " "
    segments = split_message(text)
    assert segments == ["a" * 1999]
