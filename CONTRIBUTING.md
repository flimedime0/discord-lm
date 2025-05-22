## Quick start
- clone, `python -m pip install -r requirements.txt`, `pip install -e .`
- `pre-commit install`

## Branch & PR workflow
- every change via Codex => paste instruction block, bring back diff pane
- CI must be green before merge

## Coding guidelines
- Black line length 100, Ruff rules auto-fixed
- tests in `tests/`, mark async with `pytest.mark.asyncio`

## Running the bot locally
- `python -m discord_lm_bot.discord_bot` (needs `DISCORD_TOKEN` env var)

## Releasing
- Releases are fully automated via `python-semantic-release` triggered by merges to `main`. Ensure your commit messages follow Conventional Commits style (e.g., `feat: ...`, `fix: ...`, `chore: ...`) to generate accurate changelogs and version bumps.
