import bot.main


def test_echo_command_present():
    assert 'echo' in bot.main.bot.all_commands
