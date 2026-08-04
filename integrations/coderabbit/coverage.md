# CodeRabbit Rule Coverage

This matrix keeps the compressed review profile traceable to the installable skill without copying skill-only workflow into CodeRabbit context.

| Source | CodeRabbit coverage | Treatment |
| --- | --- | --- |
| `SKILL.md` | Review baseline, architecture, security/performance | Review constraints and cross-cutting invariants included; routing, modes, tool behavior, and reference map excluded. |
| `01-source-hierarchy.md` | Review baseline and evidence | Version/source authority included; skill file-ownership guidance excluded. |
| `02-version-targeting.md` | Review baseline, Administration, payments, i18n | 6.7/6.6 compatibility checks included; research workflow and duplicated links excluded. |
| `03-implementation-workflow.md` | Architecture, testing and release validation | Coherent-change, DRY/KISS, migration, regression, and validation rules included; implementation steps and PR/QA templates excluded. |
| `04-plugin-backend.md` | Architecture, DAL/backend, cache, Messenger, security/performance | All reviewable backend invariants included and delayed-work guidance corrected. |
| `05-storefront-and-themes.md` | Storefront, cache, accessibility, security/performance | Twig/JS/SCSS/theme/cache/SEO checks consolidated. |
| `06-administration-and-apps.md` | Administration, DAL/backend | Plugin Administration, ACL, save-flow, and compatibility checks included; app/cloud architecture omitted. |
| `07-payments.md` | Payments, security/performance | Handler, authority, webhook, saved-method, refund, and operational rules included; headless architecture wording generalized. |
| `08-analysis-and-reviews.md` | Review baseline and evidence | Severity, evidence, baseline, scope, and finding classification included; literal output templates and fix-execution workflow excluded. |
| `09-symfony-and-php.md` | Architecture, Messenger, security/performance | PHP/Symfony service, client, exception, retry, and code-shape rules consolidated. |
| `10-official-docs-map.md` | Review baseline and evidence | Source-validation protocol included; URL inventory excluded. |
| `11-quality-and-operations.md` | Security/performance, operations, testing | Security, resilience, observability, readiness, queue/cache/index, and scheduled-work checks included. |
| `12-extension-patterns.md` | DAL/backend, storefront, i18n, security/performance | Config, Flow, CMS, import/export, media, rules, mail, catalog, and custom-line-item checks folded into owning review sections. |
| `13-context-and-commerce.md` | Internationalization and commerce context | Context, sales-channel, price, tax, currency, and B2B scope included. |
| `14-cli-and-dev-tooling.md` | Messenger/operations, testing | Worker, transport, command, CI, static-analysis, and debugging-artifact checks included; local command workflow excluded. |
| `15-subscriptions-and-recurring-payments.md` | Subscriptions and recurring commerce | Lifecycle, ownership, renewal, provider, snapshot, and cross-plugin rules included. |
| `16-headless-and-composable-frontends.md` | Payments, security/performance | Universal browser/server trust, bounded API, and callback rules included; composable framework and separate-frontend architecture omitted. |
| `17-accessibility-and-template-best-practices.md` | Accessibility, storefront | WCAG-oriented storefront checks consolidated; legal framing and repeated generic review prose excluded. |
| `18-cart-and-checkout-pipeline.md` | Cart and checkout | Collector, processor, validator, line-item, delivery, promotion, recalculation, hot-path, and async boundaries included. |
| `19-testing-patterns.md` | Testing and release validation | Test traits, scope, fixtures, repositories, Store API, migration, and frontend checks included with corrected fixture requirements. |
| `20-search-and-indexing.md` | Search and indexing | Search, mapping/fetch/query, indexer lifecycle, worker, fallback, and reindex rules included with the complete abstract contract. |
| `21-internationalization-and-snippets.md` | Internationalization and commerce context | Snippet, translation, language-chain, and validation checks included. |

Every numbered reference contributes at least one review criterion. Exclusions are limited to agent workflow, routing, output templates, link inventories, legal framing, or platform-specific app/composable architecture.
