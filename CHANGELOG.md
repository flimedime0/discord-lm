# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- pre-commit hooks (Black, Ruff, EOF fixer)
- Basic GitHub Actions CI (Black, Ruff, pytest).
### Fixed
- URLs are no longer split across message boundaries.
- OpenAI client initialised lazily; CI no longer needs API key.

## [0.1.0] – 2025-05-20
### Added
- Initial bot with OpenAI chat, Google CSE search, URL-safe splitter, mention trigger.
