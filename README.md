# Shopware Claude Code Skill

Claude Code skill for Shopware 6 plugin development, project implementation, code review, accessibility compliance, payment integrations, subscriptions, headless frontends, administration, testing, search/indexing, and architecture analysis.

Built for Shopware 6.7-first work with explicit 6.6 compatibility handling. Adapted from the [Shopware Codex Skill](https://github.com/biotech-shopware/shopware-codex-skill) for Claude Code.

## Design

- One installable skill: `shopware-development`
- Lean trigger file (`SKILL.md`) plus 21 focused reference files
- Official Shopware docs first, matching core behavior second
- Guardrails only, never a cap on Claude investigation depth or solution search
- Reference files loaded selectively based on task routing, not bulk-loaded

## Repository Layout

```text
claude-shopware-skill/
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
└── shopware-development/
    ├── SKILL.md
    └── references/
        ├── 01-source-hierarchy.md
        ├── 02-version-targeting.md
        ├── 03-implementation-workflow.md
        ├── 04-plugin-backend.md
        ├── 05-storefront-and-themes.md
        ├── 06-administration-and-apps.md
        ├── 07-payments.md
        ├── 08-analysis-and-reviews.md
        ├── 09-symfony-and-php.md
        ├── 10-official-docs-map.md
        ├── 11-quality-and-operations.md
        ├── 12-extension-patterns.md
        ├── 13-context-and-commerce.md
        ├── 14-cli-and-dev-tooling.md
        ├── 15-subscriptions-and-recurring-payments.md
        ├── 16-headless-and-composable-frontends.md
        ├── 17-accessibility-and-template-best-practices.md
        ├── 18-cart-and-checkout-pipeline.md
        ├── 19-testing-patterns.md
        ├── 20-search-and-indexing.md
        └── 21-internationalization-and-snippets.md
```

## Core Files

- [`shopware-development/SKILL.md`](shopware-development/SKILL.md)
  Trigger file, routing table, source order, execution rules, and reference map. Claude Code loads this when the skill is invoked and uses the Read tool to access reference files as needed.
- [`CHANGELOG.md`](CHANGELOG.md)
  Release history.
- [`LICENSE`](LICENSE)
  MIT license.

## Reference Guide

Each reference file owns one cluster of concerns. Claude reads only the files relevant to the current task, keeping context focused.

- `01-source-hierarchy.md` -- Source authority, ownership boundaries, and where new learnings belong.
- `02-version-targeting.md` -- 6.7 default behavior, 6.6 compatibility, migration playbook.
- `03-implementation-workflow.md` -- Small-step delivery, validation, regression control, PR/MR templates.
- `04-plugin-backend.md` -- Backend architecture, DAL, Store API, Admin API, HTTP cache safety, migrations, Messenger patterns, async boundaries.
- `05-storefront-and-themes.md` -- Twig, storefront JS, SCSS, theme work, cache-aware rendering, consent-aware widgets, modal patterns, accessibility basics.
- `06-administration-and-apps.md` -- Admin modules, ACL, apps, cloud/app-first tradeoffs, Vue 3/Pinia/Vite migration.
- `07-payments.md` -- Payment handlers, redirects, finalize flow, webhooks, idempotency, vaulting, refunds, payment trust boundaries.
- `08-analysis-and-reviews.md` -- Findings-first review mode, severity model (P0/P1/P2), evidence rules, triangulation reviews.
- `09-symfony-and-php.md` -- Symfony and PHP rules that matter inside Shopware projects.
- `10-official-docs-map.md` -- Official Shopware and Symfony doc links plus core-source anchors.
- `11-quality-and-operations.md` -- Security baseline, external dependency resilience, cache/queue operations, observability, testing/CI, common failure modes.
- `12-extension-patterns.md` -- Config, Flow Builder, CMS, import/export, media, mail/notification, product/catalog extensions, Rule Builder.
- `13-context-and-commerce.md` -- `Context` vs `SalesChannelContext`, pricing, tax, multichannel behavior, B2B-sensitive logic.
- `14-cli-and-dev-tooling.md` -- Console commands, worker/runtime operations, static analysis, CI, local tooling.
- `15-subscriptions-and-recurring-payments.md` -- Subscription lifecycle, renewals, saved-method ownership, recurring-flow audits.
- `16-headless-and-composable-frontends.md` -- Browser trust boundaries, separate frontend packages, backend/frontend payment contracts.
- `17-accessibility-and-template-best-practices.md` -- WCAG-oriented storefront audits, theme/accessibility pitfalls, accessibility review heuristics.
- `18-cart-and-checkout-pipeline.md` -- Cart collectors, processors, validators, line-item modeling, delivery/promotion interactions, checkout hot-path rules.
- `19-testing-patterns.md` -- Integration tests, Store API tests, fixtures, repository mocks, Shopware test traits.
- `20-search-and-indexing.md` -- Search routes, custom indexers, Elasticsearch/OpenSearch extension points, mapping/fetch symmetry, reindexing.
- `21-internationalization-and-snippets.md` -- Storefront/admin snippets, translation associations, fallback rules, 6.7 base-snippet conventions.

## Install

### Personal (all projects)

```bash
mkdir -p ~/.claude/skills
cp -R shopware-development ~/.claude/skills/
```

### Project-level (single project)

```bash
mkdir -p .claude/skills
cp -R shopware-development .claude/skills/
```

After installation, restart Claude Code so the skill is discovered. The required file for discovery is:

```text
<skills-dir>/shopware-development/SKILL.md
```

## Use in Claude Code

Invoke explicitly for reliable activation:

```text
/shopware-development review this Shopware plugin for P0/P1 security, performance, DAL, and compatibility issues
```

```text
/shopware-development implement this feature in small safe chunks and call out version-specific behavior explicitly
```

```text
/shopware-development review this payment flow with focus on validate/finalize, webhook authenticity, idempotency, and ownership
```

```text
/shopware-development review this storefront for WCAG, keyboard, focus, modal, and repeated-component issues
```

```text
/shopware-development analyze this cart or checkout change with focus on collectors, processors, pricing, delivery, and hot-path safety
```

```text
/shopware-development harden this Shopware 6.7 plugin so it stays Varnish-safe, uses Messenger/RabbitMQ correctly, and keeps indexers bounded
```

```text
/shopware-development review these subscription and PSP plugins together with focus on ownership, recurring references, renewal authority, and cross-plugin contract drift
```

```text
/shopware-development review this backend plugin and frontend checkout package together with focus on browser-authored payment data, callback authority, and server-side payment truth
```

Claude may also trigger the skill automatically from the task description when the `description` field matches, but explicit invocation is more reliable.

### Prompt patterns

**Strict plugin review:**
```text
/shopware-development review this plugin for P0/P1 security, performance, DAL, webhook, and Shopware compatibility issues. Findings first, with concrete file references.
```

**Small-step bug fix:**
```text
/shopware-development analyze this bug, identify the smallest safe fix, implement it, and validate only the affected flow first.
```

**Architecture exploration:**
```text
/shopware-development think broadly first, compare 2-3 viable approaches, then recommend the best one. Use the skill as Shopware guardrails, not as a cap on solution space.
```

**Full-repo review without constraining the model:**
```text
/shopware-development do a full end-to-end review of this Shopware project. Use the skill as context and guardrails only, not as a cap on investigation depth.
```

**PR description:**
```text
/shopware-development write a PR description for this change using the default detailed structure.
```

## How the Skill Works

1. `SKILL.md` stays lean and routes Claude to the right reference files via a routing table.
2. Claude uses the Read tool to access only the reference files relevant to the current task.
3. Reference files contain Shopware-specific guardrails, patterns, code examples, and anti-patterns.
4. The skill is context and guardrails only, not a limit on review breadth or implementation depth.
5. The inline code examples in references are anchors, not mandatory copy-paste solutions.
6. Official Shopware docs take authority when guidance conflicts with the skill.

### What the skill changes

It adds Shopware-specific guardrails:

- Which sources matter most (official docs > stable core > Symfony > skill)
- Which version assumptions are dangerous
- Which Shopware patterns are safe and which are common traps
- Which recurring bugs and security issues to look for
- Which frontend payment flows leak trust into the browser
- Which storefront accessibility and template patterns fail in real projects

### What the skill does not change

It does not replace Claude's reasoning, planning, code reading, or implementation ability. Claude still decides how to investigate the repo, which files matter, which fix is best, and how broad the solution should be.

## Relation to the Codex Skill

This skill is the Claude Code adaptation of the [Shopware Codex Skill](https://github.com/biotech-shopware/shopware-codex-skill). All 21 reference files carry the same Shopware domain content. The differences are:

- SKILL.md uses Claude Code YAML frontmatter instead of Codex metadata
- Reference loading uses Claude's Read tool with `${CLAUDE_SKILL_DIR}` paths
- `AGENTS.md` references are mapped to `CLAUDE.md`
- No `agents/openai.yaml` (Codex-specific)
- Invocation uses `/shopware-development` instead of `$shopware-development`

## Release Model

- Current release history lives in [`CHANGELOG.md`](CHANGELOG.md).
- The installable skill root is `shopware-development/`.
- The skill name is `shopware-development`.

## Maintenance

- Keep `SKILL.md` small and routing-focused.
- Put detailed guidance in the owning reference file.
- Keep examples inline with the owning rule instead of creating parallel example files.
- Update `CHANGELOG.md` for every public release.
- Do not add machine-specific paths or personal filesystem references to public files.
- When the Codex skill is updated, sync the same domain content changes here.
