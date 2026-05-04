# Changelog

All notable changes to the universal Shopware AI skill are documented in this file.

## [v0.7.0] - 2026-05-04

### Added

- Made `biotech-shopware/claude-shopware-skill` the universal Shopware skill repo for Claude Code and Codex.
- Added `shopware-development/agents/openai.yaml` so Codex can use the same installable skill folder.
- Added compact `Index:` lines to dense reference files to improve reference navigation.

### Changed

- Neutralized `shopware-development/SKILL.md` and reference wording so the installable skill content is not tied to one runtime.
- Replaced linear top-level workflow wording with mode-specific routing for planning, implementation, review, research, and PR/release summaries.
- Tightened source handling:
  - prefer `composer.json`, targeted package checks, vendor metadata, and focused lock-file searches over full `composer.lock` reads
  - treat Shopware docs as starting evidence and verify behavior-sensitive claims against matching core or installed vendor code
  - handle Symfony research across component docs, framework integration docs, and reference/config docs
- Preserved and normalized recent Codex-side additions:
  - migration immutability guidance
  - administration Twig behavior
  - temporary upload cleanup
  - sales-channel repository guidance
  - HTTP cache, queue, indexer, storefront, accessibility, and review routing
- Updated `README.md` for both Claude Code and Codex installation and invocation.

### Validated

- Installable skill markdown is runtime-neutral except permitted repo-local overlay names.
- Existing payment, recurring, headless, cart, checkout, cache, queue, indexing, accessibility, testing, i18n, backend, and review guidance remains covered.
- Public documentation contains no local machine paths.

## [v0.6.0] - 2026-04-01

### Changed

- Synced the public Shopware content to Codex `v0.6.0` while preserving Claude Code wrappers.
- Added pragmatic coding defaults:
  - smallest coherent safe change
  - DRY and KISS
  - no redundant defensive wrappers without a concrete failure mode
  - reuse existing seams over near-duplicate helpers
- Added high-impact direction-choice rules:
  - ask before choosing materially different persistence or UX approaches
  - prefer parent entity save flow by default for entity-owned admin data
- Added stable review-baseline and triage behavior:
  - pin findings to the current commit or working tree state
  - say when the baseline changed between runs
  - classify follow-up output as actionable, deferred, inactive, or verification gap
  - prefer one-finding-at-a-time remediation with narrow regression passes
- Clarified that repo-local overlays own local workflow preferences such as build policy, command restrictions, branch workflow, and project-specific dormant-feature notes.

### Validated

- Claude Code invocation and tool metadata remained intact.
- Public markdown stayed concise and user-facing.

## [v0.0.1] - 2026-03-20

### Added

- Initial Claude Code release of `shopware-development`.
- Full 21-reference Shopware skill pack for Shopware 6 implementation, review, payments, storefront, admin, operations, and architecture work.
