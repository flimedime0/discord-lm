from discord_lm_bot import database


def test_set_and_get(tmp_path, monkeypatch):
    db_file = tmp_path / "db.sqlite3"
    monkeypatch.setattr(database, "DB_PATH", db_file)
    database.setup_database()
    database.set_user_setting(1, "active_model", "o3")
    database.set_user_setting(1, "temperature", 0.5)
    settings = database.get_user_settings(1)
    assert settings["active_model"] == "o3"
    assert settings["params"]["temperature"] == 0.5


def test_get_defaults_when_missing(tmp_path, monkeypatch):
    db_file = tmp_path / "db.sqlite3"
    monkeypatch.setattr(database, "DB_PATH", db_file)
    assert database.get_user_settings(99) == {}
