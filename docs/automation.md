# Automation Pipeline

This project uses several GitHub Actions workflows to keep everything in sync:

* **CI workflow** (`.github/workflows/ci.yml`)
  * Runs on every push and pull request.
  * Installs dependencies and performs an editable install of the bot.
  * Formats and lints the code with **Black** and **Ruff**.
  * Type-checks with **Mypy**.
  * Executes unit tests with **Pytest** and uploads coverage to Codecov.
  * Builds the Docker image (without pushing).
  * Builds the documentation site and checks external links.
  * If a PR title contains a Task ID, the Issue Sync job automatically opens/labels the matching issue when the PR is merged.
* **Release workflow** (`.github/workflows/release.yml`)
  * Triggers when a pull request is merged into `main`.
  * Uses **python-semantic-release** to bump the version and update `CHANGELOG.md`.
  * Creates a Git tag and GitHub release.
  * Builds and pushes the Docker image to `ghcr.io`.
  * Runs the Issue Sync workflow to mark related issues as `status:done`.
* **Roadmap Sync** (`.github/workflows/roadmap-sync.yml`)
  * Runs on issue events such as opened, edited or closed.
  * Calls `tools/update_state.py` to regenerate `PROJECT_STATE.md`.
* **Issue Sync** (`.github/workflows/issue-sync.yml`)
  * Updates issue labels after releases to ensure the roadmap reflects completed work.
* **Dependabot** (configured via `.github/dependabot.yml`)
  * Weekly checks for outdated dependencies and opens pull requests which go through the same CI checks.

This automation keeps `main` always releasable and documentation fully up to date.
