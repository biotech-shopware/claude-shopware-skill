# Source Hierarchy

## Authority Order

1. Project version signals: root and extension `composer.json`, installed package metadata, and targeted lock-file checks when exact versions matter.
2. Official Shopware docs for the exact target version as starting evidence.
3. Stable Shopware core or installed vendor behavior matching the project version for behavior-sensitive claims.
4. Official Symfony component, framework integration, and reference docs when Symfony behavior matters.
5. This skill's distilled references.

For storefront accessibility questions, use this variant:

1. Shopware docs and matching core storefront behavior for the target version.
2. WCAG 2.2, WAI-ARIA APG, ADA.gov, and U.S. Access Board material when the question is accessibility-specific.
3. Symfony docs when framework behavior matters to the implementation.
4. This skill's distilled references.

## Core Source Verification Gate

Before naming or extending a Shopware core class, service id, route, Twig template path/block, storefront JS import, admin component/block, CLI command, event, or feature flag:

1. Resolve the target version from project files first; if none is pinned, use the latest stable Shopware release from the changelog/GitHub releases.
2. Open the matching Shopware core tag on `github.com/shopware/shopware` or installed `vendor/shopware/*` source; use `trunk` only for explicitly unreleased work.
3. Verify the exact symbol/path exists and inspect the surrounding owner pattern before implementing.
4. If docs, ADRs, beta notes, generated examples, or memory conflict with the matching core source, the matching core source wins.
5. For Twig and Administration work, inspect the actual current template/component and block names before choosing an override target.
6. If the symbol cannot be verified, state the verification gap and avoid hard-coding guessed names.
7. Cite the checked core/vendor path or URL for version-sensitive decisions in the final answer.

## Ownership Boundaries

Keep each concern in one place:

- Workflow and loading rules belong in `SKILL.md` and `03-implementation-workflow.md`.
- Version splits belong in `02-version-targeting.md`.
- General plugin and project backend rules belong in `04-plugin-backend.md`.
- Compact storefront, Twig, JS, SCSS, theme, SEO, and implementation-level accessibility rules belong in `05-storefront-and-themes.md`.
- Deep accessibility standards, WCAG-oriented audit heuristics, and storefront compliance review patterns belong in `17-accessibility-and-template-best-practices.md`.
- Administration modules, app extensions, and admin migration guidance belong in `06-administration-and-apps.md`.
- Payment-only rules belong in `07-payments.md`.
- Review/audit rules belong in `08-analysis-and-reviews.md`.
- Symfony/PHP baseline rules belong in `09-symfony-and-php.md`.
- Official links belong in `10-official-docs-map.md`.
- Security baseline, observability, testing, store-readiness, and common plugin failure patterns belong in `11-quality-and-operations.md`.
- Configuration, Flow Builder triggers, CMS patterns, import/export, media, and Rule Builder belong in `12-extension-patterns.md`.
- Context handling, multichannel behavior, pricing, and sales-channel-aware logic belong in `13-context-and-commerce.md`.
- Console commands and development tooling belong in `14-cli-and-dev-tooling.md`.
- Subscription lifecycle and recurring-commerce orchestration belong in `15-subscriptions-and-recurring-payments.md`.
- Headless or composable frontend payment and trust-boundary rules belong in `16-headless-and-composable-frontends.md`.
- Cart, checkout, delivery, line item, and promotion pipeline rules belong in `18-cart-and-checkout-pipeline.md`.
- Shopware-specific testing patterns belong in `19-testing-patterns.md`.
- Search, Elasticsearch, and OpenSearch rules belong in `20-search-and-indexing.md`.
- Snippet, translation, and localization rules belong in `21-internationalization-and-snippets.md`.
- Code review protocol, 3-pass process, report naming, and prior-review validation belong in `22-code-review-protocol.md`.
- HTTP cache, delayed invalidation, `CACHE_REWORK`, `sw-cache-hash`, and Varnish/Fastly integration belong in `23-cache-and-http-cache.md`.
- External-API caching inside cart calculation (tax, shipping, personalization) belongs in `24-external-api-caching-in-cart.md`.
- Composer patches, PHPStan/PHPCS pinning, shopware-rector, Frosh Tools, and DB-dump tooling belong in `25-patching-and-dependency-tooling.md`.
- Plugin lifecycle methods, version-bump requirements, activation ordering, and `updateDestructive` semantics belong in `26-plugin-lifecycle-and-activation.md`.

Do not repeat the same rule in multiple files unless the split would otherwise hide a critical safety boundary. Use short cross-references instead.

## Ownership Examples

Use these examples to decide where a new learning belongs:

| New learning | Primary owner | Keep elsewhere |
| --- | --- | --- |
| `searchIds()` versus `search()` in DAL loops | `04-plugin-backend.md` | short cross-reference from `18` when the loop is inside cart logic |
| collector versus processor responsibilities | `18-cart-and-checkout-pipeline.md` | short cross-reference from `04` or `07` |
| Store API functional test with `SalesChannelApiTestBehaviour` | `19-testing-patterns.md` | short cross-reference from `11` |
| extending Elasticsearch product mapping and fetch logic together | `20-search-and-indexing.md` | short cross-reference from `04` |
| `messages.en.base.json` and admin/storefront snippet ownership | `21-internationalization-and-snippets.md` | short cross-reference from `05` or `06` |
| detailed PR template or findings template | `03-implementation-workflow.md` or `08-analysis-and-reviews.md` | no duplicate second owner |

Apply repo-local `AGENTS.md` or `CLAUDE.md` guidance only when the repo already uses it or the user explicitly asks for it.

Repo-local overlay files are the right place for:

- local asset-build policy
- command execution restrictions
- branch-per-finding or branch-per-review workflow
- project-specific dormant or intentionally inactive feature notes

Keep the public skill focused on durable Shopware engineering guidance.
