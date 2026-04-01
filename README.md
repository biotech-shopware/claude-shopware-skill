# Shopware Claude Code Skill

Claude Code skill for Shopware 6 plugin development, reviews, payments, subscriptions, storefront and accessibility work, administration, testing, search/indexing, and architecture analysis.

Built for Shopware 6.7-first work with explicit 6.6 compatibility handling.

## Design

- One installable skill: `shopware-development`
- Lean `SKILL.md` plus 21 focused reference files
- Official Shopware docs first, matching core behavior second
- Guardrails only, never a cap on Claude investigation depth or solution search
- Reference files read selectively based on task routing, not bulk-loaded
- Pragmatic defaults: smallest coherent safe change, DRY/KISS, and no redundant defensive wrappers without a concrete failure mode
- High-impact direction choices are paused for confirmation when they materially change persistence, entity modeling, or admin/storefront UX
- Review mode stays findings-first, baseline-aware, and explicit about deferred, inactive, and verification-gap surfaces

## Repository Layout

```text
claude-shopware-skill/
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

## Install

### Personal

```bash
mkdir -p ~/.claude/skills
cp -R shopware-development ~/.claude/skills/
```

### Project-level

```bash
mkdir -p .claude/skills
cp -R shopware-development .claude/skills/
```

Restart Claude Code after installation. Discovery requires:

```text
<skills-dir>/shopware-development/SKILL.md
```

## Use in Claude Code

Invoke explicitly for reliable activation:

```text
/shopware-development review this Shopware plugin for P0/P1 security, performance, DAL, and compatibility issues
```

```text
/shopware-development implement this feature with the smallest coherent safe change and call out version-specific behavior
```

```text
/shopware-development review this payment flow with focus on validate/finalize, webhook authenticity, idempotency, and ownership
```

```text
/shopware-development review this storefront for WCAG, keyboard, focus, modal, and repeated-component issues
```

```text
/shopware-development analyze this cart or checkout change with focus on collectors, processors, pricing, delivery, cache safety, and hot-path boundaries
```

```text
/shopware-development harden this Shopware 6.7 plugin so it stays Varnish-safe, uses Messenger/RabbitMQ correctly, and keeps indexers bounded
```

```text
/shopware-development compare 2-3 valid admin implementation directions, explain the persistence and UX tradeoffs, and wait before choosing
```

## Prompt Patterns

**Strict plugin review**

```text
/shopware-development review this plugin for P0/P1 security, performance, DAL, webhook, and Shopware compatibility issues. Findings first, with concrete file references.
```

**Small-step bug fix**

```text
/shopware-development analyze this bug, identify the smallest coherent safe fix, reuse an existing seam if appropriate, implement it, and validate only the affected flow first.
```

**Architecture exploration**

```text
/shopware-development think broadly first, compare 2-3 viable approaches, then recommend the best one. Use the skill as Shopware guardrails, not as a cap on solution space.
```

**Full-repo review without constraining the model**

```text
/shopware-development do a full end-to-end review of this Shopware project. Use the skill as context and guardrails only, not as a cap on investigation depth.
```

**PR description**

```text
/shopware-development write a PR description for this change using the default detailed structure.
```

## What the Skill Adds

- Shopware-specific source order and routing
- Example-driven backend, storefront, payments, cart, search, and testing guidance
- Pragmatic coding defaults: DRY, KISS, and no defensive ceremony without a real failure mode
- Direction-choice discipline for high-impact admin/storefront persistence and UX decisions
- Stable review behavior with baseline notes and actionable/deferred/inactive triage

The skill does not replace Claude's reasoning. It provides Shopware context and guardrails, not a ceiling on breadth or depth.

## Repo-Local Overlay

Keep repo-specific workflow choices in `CLAUDE.md`, not in the public skill. Typical local overlays include asset-build policy, command restrictions, branch workflow, and project-specific dormant-feature notes.

## Release Model

- Release history lives in [CHANGELOG.md](CHANGELOG.md).
- The installable skill root is `shopware-development/`.
- The skill name is `shopware-development`.
