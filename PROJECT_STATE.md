## Current architecture
- config
- openai_client
- splitter
- discord_bot

## Completed tasks
- precommit-setup-07
- ci-basic-11
- fix-link-split-42
- test-splitter-12
- fix-ci-openai-24
- logging-retry-15

## Backlog
| ID | Scope | Status |
| dockerize-13 | Dockerfile & compose | next |
| mypy-baseline-14 | add type hints & mypy | queued |
| docs-mkdocs-17 | nice docs site | queued |
| coverage-18 | pytest-cov, badge | queued |
| dependabot-release-16 | weekly bumps, semantic-release | queued |

## Key decisions
- why lazy OpenAI client with dummy key
- why splitter extracted from send_slow_message
