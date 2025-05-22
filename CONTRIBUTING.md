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
- bump CHANGELOG, tag once CI passes (semantic-release TBD)

## Bootstrapping Historical Issues
This project uses GitHub Issues to track tasks, which then auto-populates PROJECT_STATE.md.
To create issues for work completed before this system was in place, run the `tools/create_historical_issues.py` script once from your Codespace terminal.
Ensure you are authenticated with the gh CLI (`gh auth login`) and have write permissions for issues on this repository.
