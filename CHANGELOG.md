# Changelog

All notable changes to the universal Shopware AI skill are documented in this file.

## [v0.7.3] - 2026-08-04

### Added

- Added `integrations/coderabbit/shopware-review.md`, a 3,000-4,000 word review-only profile for CodeRabbit coding guidelines.
- Added a source-coverage matrix mapping every skill reference to included, consolidated, or intentionally excluded CodeRabbit criteria.
- Added README installation guidance for using the profile as `.rules/shopware-review.md` without unnecessary CodeRabbit YAML.

### Corrected

- Replaced the generic Symfony `DelayStamp` recommendation with Shopware transport-safe delayed-work guidance.
- Replaced incomplete product and `StaticEntityRepository` test examples with complete, contract-shaped fixtures.
- Completed the custom `EntityIndexer` example with the full 6.6/6.7 abstract lifecycle and preserved write context.

### Validated

- Verified the corrected indexer contract against Shopware `v6.7.12.2` and `v6.6.10.21` stable core tags.
- Verified Shopware's `NoDelayStampRule` rejects `DelayStamp` because it is not compatible with every supported Messenger transport.
- Confirmed every numbered reference contributes review criteria while skill-only routing, implementation workflow, output templates, link inventories, and platform-specific app/composable architecture remain outside the CodeRabbit profile.

## [v0.7.2] - 2026-05-16

### Changed

- Added a core-source verification gate for named Shopware classes, service ids, routes, Twig paths/blocks, storefront imports, Administration components/blocks, CLI commands, events, and feature flags.
- Strengthened fallback version handling: when a project does not pin Shopware, use the latest stable Shopware changelog/GitHub release tag instead of `trunk`, beta notes, ADR memory, generated examples, or old docs.
- Kept the installable skill runtime-neutral for Claude and Codex while preserving the shared `shopware-development/agents/openai.yaml` Codex metadata.

### Validated

- Confirmed the guardrail is owned by `references/01-source-hierarchy.md` with only a short pointer in `SKILL.md` and README.
- Confirmed the current stable Shopware release source exposes the 6.7 buy widget at `src/Storefront/Resources/views/storefront/component/buy-widget/buy-widget.html.twig` with `buy_widget_ordernumber_container`.

## [v0.7.1] - 2026-05-06

### Changed

- Normalized `allowed-tools` in `shopware-development/SKILL.md` to an explicit YAML list for Claude Code compatibility.
- Converted the `SKILL.md` reference map to relative Markdown links and clarified that numeric routing entries map to those references.
- Shortened `shopware-development/agents/openai.yaml` `default_prompt` while keeping the full Shopware scope in metadata.
- Polished README installation guidance for Claude Code CLI/app, Claude native app/web, Codex IDE, Codex CLI, and the native Codex Mac app.

### Validated

- GitHub `main` and tagged installs work through the Codex skill installer.
- Codex CLI smoke test routes Varnish plus RabbitMQ work to `04`, `05`, `11`, and `14`.
- Claude Code CLI support is validated by package shape and official discovery paths on this machine because the `claude` binary is not installed.

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
- Updated `README.md` with install and invocation guidance for Claude Code CLI/app, Claude native app/web, Codex CLI, Codex IDE, and the native Codex Mac app.

### Validated

- Installable skill markdown is runtime-neutral except permitted repo-local overlay names.
- Existing payment, recurring, headless, cart, checkout, cache, queue, indexing, accessibility, testing, i18n, backend, and review guidance remains covered.
- Dry-run local installs resolve the expected Claude Code and Codex skill files.
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
