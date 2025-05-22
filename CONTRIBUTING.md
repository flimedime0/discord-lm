## Quick start
- clone, `python -m pip install -r requirements.txt`, `pip install -e .`
- `pre-commit install`

## Branch & PR workflow
- every change via Codex => paste instruction block, bring back diff pane
- CI must be green before merge
- every PR **must** include a Task ID and tests or a justification

## Coding guidelines
- Black line length 100, Ruff rules auto-fixed
- tests in `tests/`, mark async with `pytest.mark.asyncio`

### Writing tests

Use `pytest` along with `pytest-mock` for patches:

```python
def test_example(monkeypatch):
    monkeypatch.setattr(module, "func", lambda: 42)
    assert run() == 42
```

## Running the bot locally
- `python -m discord_lm_bot.discord_bot` (needs `DISCORD_TOKEN` env var)

## Releasing
- Releases are fully automated via **python-semantic-release** on every merge to **main**. Use Conventional Commit messages (`feat: …`, `fix: …`, `chore: …`) so the changelog & version bump are generated correctly.

## Bootstrapping Historical Issues
Run `gh auth login` to authenticate, then execute:

```bash
python tools/create_historical_issues.py
```

This scans `CHANGELOG.md` for completed tasks and creates GitHub issues for them once.
