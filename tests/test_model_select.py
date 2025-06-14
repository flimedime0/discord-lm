from unittest import mock

import pytest

from discord_lm_bot import database
from discord_lm_bot.ui_model_select import ModelSelect


@pytest.mark.asyncio
async def test_model_select_updates_db(tmp_path, monkeypatch):
    db_file = tmp_path / "db.sqlite3"
    monkeypatch.setattr(database, "DB_PATH", db_file)
    database.setup_database()

    view = ModelSelect(user_id=42)
    interaction = mock.Mock()
    interaction.response.edit_message = mock.AsyncMock()
    dummy_select = mock.Mock()
    dummy_select.values = ["gpt-4o"]

    await ModelSelect.select(view, interaction, dummy_select)

    settings = database.get_user_settings(42)
    assert settings["active_model"] == "gpt-4o"
