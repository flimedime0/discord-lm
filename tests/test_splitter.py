from discord_lm_bot.splitter import split_message


def test_split_message_no_url_split():
    base = "x" * 1995
    url = " https://example.com/test"
    segs = split_message(base + url)
    assert segs == [base, url.strip()]


def test_split_message_no_blank_segment():
    text = "a" * 1999 + " "
    assert split_message(text) == ["a" * 1999]


def test_split_message_unicode_and_urls():
    text = "あ" * 1000 + " https://example.com/foo" + " bar"
    parts = split_message(text, max_len=1005)
    assert parts == ["あ" * 1000, "https://example.com/foo bar"]


def test_split_message_no_break_space():
    nbsp = "a" * 1000 + "\xa0" + "b" * 1000
    parts = split_message(nbsp, max_len=1000)
    assert parts == ["a" * 1000, "b" * 1000]


def test_split_message_suffix_len():
    text = "x" * 1995
    parts = split_message(text, suffix_len=10)
    assert all(len(p) <= 1990 for p in parts)
