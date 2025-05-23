# CHANGELOG

## Unreleased

### Added

- PR-title lint workflow prevents merges without a Task ID.

### Fixed

- Correct indentation and duplicate lines in `issue-sync.yml`; workflow now parses.
- Remove indented here-doc in `issue-sync.yml`; workflow now runs without IndentationError.

## v0.3.2 (2025-05-22)

### Bug Fixes

- **ci**: Repair issue-sync workflow
  ([`b77d13f`](https://github.com/flimedime0/discord-lm-app/commit/b77d13fc66b7739502a9f0cac5b87dcd0120dc7c))


## v0.3.1 (2025-05-22)

### Bug Fixes

- Clean issue-sync workflow and ignore egg-info
  ([`13d57b7`](https://github.com/flimedime0/discord-lm-app/commit/13d57b73950626b026693b8ef790a6c079b31255))

### Continuous Integration

- Use built-in token for issue sync
  ([`fb13d94`](https://github.com/flimedime0/discord-lm-app/commit/fb13d941141b288c0690d491fd035ea97f168fb3))

### Documentation

- Wrap badges with links
  ([`688338e`](https://github.com/flimedime0/discord-lm-app/commit/688338e6a52a7b194044701e31f63e363be4dfbb))


## v0.3.0 (2025-05-22)

### Documentation

- Sync automation docs
  ([`385cc87`](https://github.com/flimedime0/discord-lm-app/commit/385cc8770ca7a3a2fca3fd37aa9a898674b4f14e))

### Features

- Add CI and testing enhancements
  ([`3073fb0`](https://github.com/flimedime0/discord-lm-app/commit/3073fb07955c65f0bf01a363dffecc02791bbf0e))


## v0.2.0 (2025-05-22)

### Chores

- Sync automation docs and config
  ([`27fa049`](https://github.com/flimedime0/discord-lm-app/commit/27fa0490824d3609fd3e0f1e5d3b7c50576425b3))

### Continuous Integration

- Sync roadmap [skip ci]
  ([`8d15857`](https://github.com/flimedime0/discord-lm-app/commit/8d158577b6dcf6e04c9d2f03afc7209803abf1fb))

### Documentation

- Note docs-build indentation fix
  ([`284f9d2`](https://github.com/flimedime0/discord-lm-app/commit/284f9d28cc2a5cfd0b6a6b10086c7c19db6d42fa))

### Features

- Add script to create historical issues
  ([`afcab0d`](https://github.com/flimedime0/discord-lm-app/commit/afcab0dd705d94a72fbbde56f17ae1528aa20ff8))


## v0.1.1 (2025-05-22)

### Bug Fixes

- **release**: Push images
  ([`a8569b8`](https://github.com/flimedime0/discord-lm-app/commit/a8569b8ebaa61ebab2de648312af85160716ba61))

### Chores

- Tidy requirements
  ([`9dfe7d3`](https://github.com/flimedime0/discord-lm-app/commit/9dfe7d35039daf9014932f7d0eb2ed390a88dbde))

### Continuous Integration

- Install linkcheck for docs
  ([`a7c716c`](https://github.com/flimedime0/discord-lm-app/commit/a7c716cf2309cff9e6f05145e963d5e1c6f05a18))

### Documentation

- Document release docker push and coverage guard
  ([`55299ff`](https://github.com/flimedime0/discord-lm-app/commit/55299fff07da7fd2f5424cbd884068382acdc8b0))

- Fix CI badge URL
  ([`f8e06f5`](https://github.com/flimedime0/discord-lm-app/commit/f8e06f5de13f30c3a44aa0a92029d7b8b76d6e98))


## v0.1.0 (2025-05-21)

### Features

- Add roadmap sync
  ([`0b2f374`](https://github.com/flimedime0/discord-lm-app/commit/0b2f374445217961609cd7eee674d401278652ab))


## v0.0.1 (2025-05-21)

### Bug Fixes

- Fetch full history for release
  ([`8cd2633`](https://github.com/flimedime0/discord-lm-app/commit/8cd26334486b410c5f2a63e7a70b223720e48ff9))

- Preserve URLs in slow send
  ([`7edac89`](https://github.com/flimedime0/discord-lm-app/commit/7edac8908a902d4366bd78b286548694e5dd108c))

### Chores

- Add dependabot and release workflow
  ([`b4fbdda`](https://github.com/flimedime0/discord-lm-app/commit/b4fbdda3cc866221f9e3f9ba6959a93e42739028))

### Documentation

- Add contribution and project state
  ([`aeb426d`](https://github.com/flimedime0/discord-lm-app/commit/aeb426d61712368ed82c1b1360b947798f23b589))

- Clarify web search usage
  ([`2f2eee1`](https://github.com/flimedime0/discord-lm-app/commit/2f2eee1d6bfdbb975d9b5f7575df2774fa2b361c))

- Fix links for mkdocs strict
  ([`c122b71`](https://github.com/flimedime0/discord-lm-app/commit/c122b71a999cf90fdd1bd4b80cd3519cf128ea23))

- Note message content intent
  ([`18405cb`](https://github.com/flimedime0/discord-lm-app/commit/18405cb7133101df62586a8c8875395ffe51ee7f))

### Refactoring

- Lazily init openai client
  ([`da4aa5e`](https://github.com/flimedime0/discord-lm-app/commit/da4aa5eaf6709076b1aaf8187bb5aec329a36ba5))
