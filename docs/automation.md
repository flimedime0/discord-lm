# Automation pipeline

This project uses GitHub Actions for CI and release automation.

CI stages run in sequence:
1. Lint
2. Tests
3. Coverage check
4. Docs build
5. Docker build
6. Release

Dependabot sends weekly dependency bump PRs.

semantic-release tags each version and publishes GitHub Releases.

The roadmap-sync workflow rewrites `PROJECT_STATE.md` from issues.

An auto-issue workflow ensures Task-ID issues exist and are marked done when PRs merge.
