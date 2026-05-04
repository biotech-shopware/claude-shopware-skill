# Shopware AI Skill for Claude Code and Codex

Universal Shopware 6 skill for AI-assisted planning, implementation, refactoring, review, and release work.

The installable skill folder is platform-neutral. Claude Code and Codex use the same `shopware-development/` content; only installation and invocation differ by runtime.

## Scope

- Shopware 6.7-first plugin development with explicit 6.6 compatibility handling
- backend, DAL, migrations, Store API, Admin API, HTTP cache, Varnish, queues, and indexers
- storefront Twig, JS, SCSS, themes, accessibility, snippets, and i18n
- administration modules, apps, app scripts, ACL, Vue 3, Pinia, Vite, and cloud constraints
- payments, webhooks, refunds, saved methods, recurring payments, and headless contracts
- cart, checkout, delivery, promotion, testing, search, operations, and multi-plugin reviews
- pragmatic coding defaults: smallest coherent safe change, DRY/KISS, and no defensive ceremony without a concrete failure mode

## Repository Layout

```text
claude-shopware-skill/
├── CHANGELOG.md
├── LICENSE
├── README.md
└── shopware-development/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
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

### Claude Code

Personal install:

```bash
mkdir -p ~/.claude/skills
cp -R shopware-development ~/.claude/skills/
```

Project install:

```bash
mkdir -p .claude/skills
cp -R shopware-development .claude/skills/
```

Invoke explicitly:

```text
/shopware-development review this Shopware plugin for P0/P1 security, performance, DAL, and compatibility issues
```

### Codex

Install from GitHub repo `biotech-shopware/claude-shopware-skill` with skill path `shopware-development`.

Use:

```text
$shopware-development implement this Shopware 6.7 change with the smallest coherent safe change and call out version-specific behavior
```

The `shopware-development/agents/openai.yaml` file provides Codex UI metadata. The runtime skill content remains the same.

## Prompt Patterns

```text
/shopware-development review this payment flow with focus on validate/finalize, webhook authenticity, idempotency, and ownership.
```

```text
$shopware-development analyze this cart or checkout change with focus on collectors, processors, pricing, delivery, cache safety, and hot-path boundaries.
```

```text
/shopware-development review this storefront for WCAG, keyboard, focus, modal, repeated-component, and template override issues.
```

```text
$shopware-development harden this Shopware 6.7 plugin so it stays Varnish-safe, uses Messenger/RabbitMQ correctly, and keeps indexers bounded.
```

```text
/shopware-development compare 2-3 valid admin implementation directions, explain persistence and UX tradeoffs, and wait before choosing.
```

```text
$shopware-development do a full end-to-end review. Use the skill as Shopware guardrails only, not as a cap on investigation depth.
```

## Source Policy

- Detect project version from `composer.json` first.
- Use targeted package checks, vendor metadata, or focused `composer.lock` search only when exact installed versions matter.
- Treat Shopware docs as starting evidence; verify behavior-sensitive guidance against matching core or installed vendor code.
- For Symfony behavior, check component docs, framework or bundle integration docs, and reference or config docs.
- Keep local workflow preferences in repo overlays such as `AGENTS.md` or `CLAUDE.md`.

## Release Model

- Release history lives in [CHANGELOG.md](CHANGELOG.md).
- The installable skill root is `shopware-development/`.
- The skill trigger is `shopware-development`.
- Existing Claude and Codex-specific repos should not diverge from this universal skill content after `v0.7.0`.
