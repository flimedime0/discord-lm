# Automation Pipeline

This project leverages GitHub Actions to automate most of the development lifecycle:

*   **On every `git push` to any branch or `pull_request`**:
    *   The CI workflow (`.github/workflows/ci.yml`) runs.
    *   It installs dependencies (including an editable install of the bot package).
    *   Lints code with Black and Ruff.
    *   Type-checks with Mypy.
    *   Runs unit tests with Pytest and uploads coverage to Codecov.
    *   Builds the Docker image (but does not push it).
    *   Builds the MkDocs documentation site (including an external link check).
*   **On `pull_request` merged to `main`**:
    *   The Release workflow (`.github/workflows/release.yml`) runs.
    *   `python-semantic-release` determines the new version based on Conventional Commit messages.
    *   `pyproject.toml` version is bumped.
    *   `CHANGELOG.md` is updated.
    *   A Git tag and GitHub Release are created.
    *   The Docker image is built and pushed to `ghcr.io/flimedime0/discord-lm-app:<tag>`.
    *   The Issue Sync workflow (`.github/workflows/issue-sync.yml`) runs to ensure any linked GitHub Issue (via PR title Task ID) is labeled `status:done`.
*   **On GitHub `issues` events (opened, edited, labeled, closed, reopened)**:
    *   The Roadmap Sync workflow (`.github/workflows/roadmap-sync.yml`) runs.
    *   `tools/update_state.py` fetches all issues labeled `Task-ID`.
    *   `PROJECT_STATE.md` is regenerated and committed back to the repository.
*   **Weekly (via `.github/dependabot.yml`)**:
    *   Dependabot checks for outdated Python dependencies and opens PRs to update them. These PRs go through the same CI checks.

This setup ensures that `main` is always in a releasable state, documentation is current, and project status is transparent.
