# Changelog

All notable changes to the Shopware Claude Code Skill are documented in this file.

## [v0.6.0] - 2026-04-01

### Changed

- Synced the public Shopware content to Codex `v0.6.0` while keeping Claude-specific wrappers intact.
- Added pragmatic coding defaults in `shopware-development/SKILL.md`, `03-implementation-workflow.md`, `04-plugin-backend.md`, and `09-symfony-and-php.md`:
  - smallest coherent safe change
  - explicit DRY and KISS guidance
  - no redundant defensive wrappers without a concrete failure mode
  - reuse of existing seams over near-duplicate helpers
- Added high-impact direction-choice rules in `shopware-development/SKILL.md`, `04-plugin-backend.md`, `06-administration-and-apps.md`, and `12-extension-patterns.md`:
  - ask before choosing materially different persistence or UX approaches
  - prefer parent entity save flow by default for entity-owned admin data
- Added stable review-baseline and triage behavior in `shopware-development/SKILL.md` and `08-analysis-and-reviews.md`:
  - pin findings to the current commit or working tree state
  - say when the baseline changed between runs
  - classify follow-up output as actionable, deferred, inactive, or verification gap
  - prefer one-finding-at-a-time remediation with narrow regression passes
- Clarified in `01-source-hierarchy.md` that repo-local `CLAUDE.md` owns local workflow preferences such as build policy, command restrictions, branch workflow, and project-specific dormant-feature notes.
- Refreshed `README.md` to describe the current scope and Claude-specific usage without stale release references.

### Validated

- Claude-specific wrappers remain intact:
  - `allowed-tools: Read, Glob, Grep`
  - `${CLAUDE_SKILL_DIR}` reference paths
  - `Read` semantics
  - `CLAUDE.md` overlay naming
  - `/shopware-development` invocation
- No Codex-only files or wording were introduced.
- Public markdown stays concise and user-facing.

## [v0.0.1] - 2026-03-20

### Added

- Initial Claude Code release of `shopware-development`.
- Claude-specific `SKILL.md` frontmatter with `allowed-tools: Read, Glob, Grep`.
- Full 21-reference Shopware skill pack adapted for Claude Code usage.
- `${CLAUDE_SKILL_DIR}` reference loading and `CLAUDE.md` overlay naming.
