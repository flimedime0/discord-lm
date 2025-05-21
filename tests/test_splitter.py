from discord_lm_bot.splitter import split_message


def test_split_message_no_url_split():
    base = "x" * 1995
    url = " https://example.com/test"
    segs = split_message(base + url)
    assert segs == [base, url.strip()]


def test_split_message_no_blank_segment():
    text = "a" * 1999 + " "
    assert split_message(text) == ["a" * 1999]
