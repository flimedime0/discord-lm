# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- pre-commit hooks (Black, Ruff, EOF fixer)
- Basic GitHub Actions CI (Black, Ruff, pytest).
- CONTRIBUTING and project state docs.
- Dockerfile & docker-compose for one-command run.
- CI job that builds the image.
- mypy static-type checking (CI + pre-commit).
- Structured Rich logging and exponential-back-off retries for OpenAI & Google calls.
- MkDocs documentation site (Material theme) and CI build.
- Coverage reporting with pytest-cov + Codecov badge.
 - Automated dependency updates via Dependabot
 - Semantic-release workflow (auto version + GitHub Release notes)
### Fixed
- URLs are no longer split across message boundaries.
- OpenAI client initialised lazily; CI no longer needs an API key.
- CI passes when no tests are collected.
- Release workflow now fetches full git history (semantic-release works).

## [0.1.0] – 2025-05-20
### Added
- Initial bot with OpenAI chat, Google CSE search, URL-safe splitter, mention trigger.
