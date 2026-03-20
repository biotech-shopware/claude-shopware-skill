# Changelog

All notable changes to the Shopware Claude Code Skill are documented in this file.

## [0.0.1] - 2026-03-20

### Added

- Initial Claude Code skill release, adapted from [Shopware Codex Skill v0.5.0](https://github.com/biotech-shopware/shopware-codex-skill).
- `SKILL.md` with Claude Code YAML frontmatter (`name`, `description`, `allowed-tools`), task routing table, execution rules, and reference map.
- All 21 reference files carried over from the Codex skill with full Shopware 6 domain coverage:
  - `01` Source hierarchy and ownership boundaries.
  - `02` Version targeting (6.7 default, 6.6 compatibility, migration playbook).
  - `03` Implementation workflow, chunking, PR/MR templates.
  - `04` Plugin backend architecture, DAL, Store API/Admin API, HTTP cache safety, migrations, Messenger patterns.
  - `05` Storefront and themes (Twig, JS, SCSS, cache-aware rendering, consent-aware widgets).
  - `06` Administration and apps (ACL, cloud/app-first, Vue 3/Pinia/Vite).
  - `07` Payments (handlers, webhooks, idempotency, vaulting, refunds, trust boundaries).
  - `08` Analysis and reviews (findings-first, severity model, triangulation).
  - `09` Symfony and PHP baseline rules.
  - `10` Official docs map with versioned links and core-source anchors.
  - `11` Quality and operations (security, resilience, observability, common failure modes).
  - `12` Extension patterns (config, Flow Builder, CMS, import/export, media, Rule Builder).
  - `13` Context and commerce (SalesChannelContext, pricing, tax, multichannel, B2B).
  - `14` CLI and dev tooling (console commands, workers, static analysis).
  - `15` Subscriptions and recurring payments (lifecycle, renewal, saved-method ownership).
  - `16` Headless and composable frontends (browser trust, payment contracts).
  - `17` Accessibility and template best practices (WCAG, storefront audits, anti-patterns).
  - `18` Cart and checkout pipeline (collectors, processors, validators, line items, delivery).
  - `19` Testing patterns (integration tests, Store API tests, fixtures, test traits).
  - `20` Search and indexing (Elasticsearch/OpenSearch, custom indexers, mapping).
  - `21` Internationalization and snippets (storefront/admin snippets, translation associations).
- `AGENTS.md` references updated to `CLAUDE.md` for Claude Code compatibility.
- `allowed-tools: Read, Glob, Grep` for automatic reference file access without permission prompts.
- Reference loading uses `${CLAUDE_SKILL_DIR}/references/` paths for Claude's Read tool.

### Adapted from Codex

- Codex `$shopware-development` invocation mapped to Claude Code `/shopware-development`.
- Codex `agents/openai.yaml` UI metadata replaced by SKILL.md YAML frontmatter.
- Codex "load" semantics mapped to Claude Code Read tool semantics.
- All Shopware domain content (execution rules, patterns, code examples, anti-patterns) preserved without modification.

### Validated

- Grep for stale terms (`Codex`, `AGENTS.md`, `$shopware-development`, `openai.yaml`) returns zero matches in the skill directory.
- All 21 reference file names match the Codex source exactly.
- Content parity confirmed: only `01-source-hierarchy.md` and `03-implementation-workflow.md` differ (AGENTS.md to CLAUDE.md substitution).
