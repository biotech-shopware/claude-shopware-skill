---
name: shopware-development
description: >-
  Plan, implement, refactor, or review Shopware 6 changes with Shopware 6.7
  as the default target and explicit Shopware 6.6 compatibility handling.
  Use for plugin development, cart and checkout pipeline work, theme and
  template work, storefront Twig/JS/SCSS changes, accessibility or storefront
  compliance reviews, headless or composable frontend integrations,
  administration modules, app extensions, payment integrations, subscriptions
  and recurring-commerce flows, saved-payment-method ownership issues, testing
  patterns, search and indexing work, i18n and snippet handling, CMS elements,
  import/export work, media handling, Rule Builder conditions, CLI and tooling
  tasks, multichannel context issues, project implementation planning,
  migrations, performance/security hardening, and Shopware code reviews or
  multi-plugin architecture analysis.
allowed-tools: Read, Glob, Grep
---

# Shopware Development

## Hard Constraints

- This skill must not cap investigation depth, reasoning depth, or solution breadth when the request or evidence requires more.
- Treat reference files as starting context. Keep following code, config, adjacent repos, official docs, and source evidence until the relevant surface is exhausted.
- Keep public guidance durable. Repo-local workflow preferences belong in `AGENTS.md` or `CLAUDE.md` when the repo uses those files.

## Source Rules

1. Detect target version from root and extension `composer.json` first.
2. Use targeted package checks, vendor metadata, or focused `composer.lock` search only when exact installed versions matter. Do not read the full lock file by default.
3. Use Shopware docs as starting evidence, then verify behavior-sensitive claims against matching Shopware core or installed vendor code.
4. For Symfony behavior, check component docs, framework or bundle integration docs, and reference or config docs before concluding.
5. Treat ADRs, issues, forums, blogs, and attached material as context unless they match official docs or stable source behavior.

## Routing

Read the smallest useful set of references before broadening:

| Task signal | Always read | Also read if |
| --- | --- | --- |
| `payment`, `PSP`, `webhook`, `refund`, `vault` | `07` | `15` recurring, `16` separate frontend, `18` cart/checkout coupling |
| `cart`, `checkout`, `line item`, `delivery`, `promotion` | `18` | `04` backend, `07` payment, `13` pricing scope |
| `Twig`, `storefront`, `theme`, `SCSS`, `storefront JS` | `05` | `17` accessibility, `16` separate frontend |
| `cache`, `http cache`, `varnish`, `reverse proxy` | `04`, `05`, `11` | `10` exact docs and core anchors |
| `admin`, `app`, `cloud`, `manifest`, `Pinia`, `Vite` | `06` | `02` migration/version split, `21` snippets |
| `queue`, `messenger`, `rabbitmq`, `worker`, `async` | `04`, `11`, `14` | `18` checkout handoff, `20` indexer workers |
| `review`, `audit`, `analysis` | `08` | domain refs matching the touched flow |
| `test`, `PHPUnit`, `fixture`, `Store API test` | `19` | `18` cart, `07` payments, `20` indexing |
| `search`, `OpenSearch`, `Elasticsearch`, `listing` | `20` | `04` DAL, `13` commerce scope |
| `indexer`, `reindex`, `dal:refresh:index` | `20` | `11` operations, `14` workers/commands |
| `snippet`, `translation`, `locale`, `i18n` | `21` | `05` storefront, `06` admin, `02` 6.7.3+ base snippets |

Accessibility, ADA, WCAG, VPAT, screen reader, keyboard, form, focus, modal, storefront UX, or frontend audit tasks always read `05`, `10`, and `17`.

## Mode Workflow

| Mode | Do |
| --- | --- |
| Planning | Identify version, extension surface, hot path, source uncertainty, and 2-3 viable approaches when direction changes materially. |
| Implementation/refactor | Choose the extension point, make the smallest coherent safe change, preserve existing patterns, validate the narrowest useful surface. |
| Review/audit | Pin the baseline, scan the full affected flow, report findings first by severity/blast radius, separate actionable, deferred, inactive, and verification-gap items. |
| Research | Use docs plus matching source code. Prefer Markdown-source docs when doing detailed research. Cite exact docs or core anchors when behavior is version-sensitive. |
| PR/release summary | Use the detailed structure in `03`; use review output rules from `08` when writing findings. |

Before proposing or editing, inventory mutation surfaces, trust boundaries, ownership boundaries, browser-authored data, cross-plugin contracts, hot paths, and accessibility-sensitive UI patterns that apply to the task.

## Cross-Cutting Rules

- Default to Shopware 6.7. Read 6.6 compatibility notes only when the project or request requires them.
- Prefer the smallest coherent safe change over the mechanically smallest diff. Apply DRY and KISS by default.
- Add safeguards only for concrete failure modes in the actual code path.
- Ask before choosing between valid approaches when the choice materially changes save behavior, persistence flow, entity modeling, native-component reuse, or admin/storefront UX.
- Protect cart, checkout, login, account, renewal, cache, queue, indexer, payment, and large admin-list hot paths.
- Never trust client-reported payment state, amount, provider references, ownership, or recurring authority.
- Keep controllers, subscribers, handlers, templates, and admin UIs thin; move behavior into services or the owning extension point.
- Validate after each chunk with the narrowest useful checks and report remaining risk.

## Reference Map

- `references/01-source-hierarchy.md` source order, ownership, repo-local overlays
- `references/02-version-targeting.md` 6.7/6.6 splits, migration behavior
- `references/03-implementation-workflow.md` chunking, validation, PR/QA templates
- `references/04-plugin-backend.md` backend, DAL, APIs, cache, migrations, queues
- `references/05-storefront-and-themes.md` Twig, JS, SCSS, themes, cache-safe rendering
- `references/06-administration-and-apps.md` admin modules, ACL, apps, Vue 3, Pinia, Vite
- `references/07-payments.md` payment handlers, webhooks, saved methods, refunds
- `references/08-analysis-and-reviews.md` review mode, severity, evidence, output
- `references/09-symfony-and-php.md` PHP and Symfony rules inside Shopware
- `references/10-official-docs-map.md` docs research protocol and source anchors
- `references/11-quality-and-operations.md` security, operations, observability, store readiness
- `references/12-extension-patterns.md` config, Flow Builder, CMS, import/export, media, mail, catalog, rules
- `references/13-context-and-commerce.md` context, sales-channel scope, pricing, tax
- `references/14-cli-and-dev-tooling.md` console, workers, static analysis, local tooling
- `references/15-subscriptions-and-recurring-payments.md` subscriptions, renewals, saved-method ownership
- `references/16-headless-and-composable-frontends.md` composable frontend trust boundaries
- `references/17-accessibility-and-template-best-practices.md` WCAG storefront review and remediation
- `references/18-cart-and-checkout-pipeline.md` collectors, processors, validators, delivery, promotions
- `references/19-testing-patterns.md` integration tests, Store API tests, fixtures, mocks, migrations
- `references/20-search-and-indexing.md` search, indexers, Elasticsearch/OpenSearch, reindexing
- `references/21-internationalization-and-snippets.md` snippets, translations, fallback inheritance
