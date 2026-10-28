---
name: shopware-development
description: >-
  Review, plan, implement, refactor, or debug Shopware 6 changes. Targets
  Shopware 6.7 with explicit 6.6 compatibility handling. Covers plugin
  backend and DAL, plugin lifecycle and version bumps, cart and checkout
  pipeline, payments (AbstractPaymentHandler), subscriptions and recurring
  flows, HTTP cache and delayed invalidation, Varnish, Messenger queues,
  custom indexers, Elasticsearch/OpenSearch, CMS elements and blocks
  (Shopping Experiences), storefront Twig/JS/SCSS,
  administration (Meteor, Pinia, Vite), app extensions, Store API and Admin
  API, snippets and i18n, accessibility (WCAG/EAA), headless frontends,
  code review with a 3-pass protocol, multi-plugin audits, and the local
  shopware-cli Docker environment.
when_to_use: >-
  Use for any Shopware 6 question, whether or not a file is open. Trigger
  phrases: "review my Shopware plugin", "audit this Shopware code", "fix
  Shopware cart / checkout / payment / cache", "add a Shopware payment
  handler", "migrate 6.6 to 6.7", "why didn't my migration or custom field
  installer run", "why is Shopware invalidating too much cache", "Shopware
  Twig template", "Shopware Meteor / Pinia / Vite", "Shopware accessibility
  audit", "Store API extension", "shopware indexer / reindex", "shopware
  snippet / translation", "Shopware CMS element / block", "slot config",
  "shopware-cli project dev", "local Shopware
  Docker environment".
argument-hint: "[plan|implement|review|audit|research] <task description>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash(git status *)
  - Bash(git diff *)
  - Bash(git log *)
  - Bash(git show *)
  - Bash(git blame *)
  - Bash(composer show *)
  - Bash(composer why *)
  - Bash(composer audit *)
  - Bash(bin/console debug:* *)
  - Bash(bin/console dal:validate *)
  - Bash(bin/console cache:watch:delayed *)
  - Bash(bin/console cache:clear:delayed *)
  - Bash(bin/console messenger:stats *)
  - Bash(bin/console messenger:failed:show *)
  - Bash(bin/console framework:schema *)
  - Bash(bin/console scheduled-task:list *)
  - Bash(bin/console translation:list *)
  - Bash(bin/console translation:validate *)
  - Bash(bin/console feature:list *)
---

# Shopware Development

## Hard Constraints

- Never cap investigation depth, reasoning depth, or solution breadth when the request or evidence needs more.
- Treat reference files as starting context. Keep following code, config, adjacent repos, official docs, and source evidence until the relevant surface is exhausted.
- Keep public guidance durable. Repo-local workflow preferences belong in `AGENTS.md` or `CLAUDE.md` when the repo uses those files.
- Never invent Shopware behavior. Verify with the target-version core source or official docs before naming a class, service, route, block, or feature flag (see `references/01-source-hierarchy.md`).

## Source Rules

1. Detect the target version from root and extension `composer.json` first.
2. Use targeted package checks, vendor metadata, or focused `composer.lock` searches only when installed versions are behavior-critical. Do not read the full lock file by default.
3. Start with Shopware docs, then verify behavior-sensitive claims against matching Shopware core or installed vendor code.
4. For Symfony behavior, check component docs, framework or bundle integration docs, and reference or config docs before concluding.
5. Treat ADRs, issues, forums, blogs, and attached material as context unless they match official docs or stable source behavior.

## Routing

When the routing matrix points to a number like `07`, open `references/07-payments.md` with the Read tool before starting the task. Read the smallest useful set of references first, then broaden if evidence demands it.

| Task signal | Always read | Also read if |
| --- | --- | --- |
| `payment`, `PSP`, `webhook`, `refund`, `vault`, `AbstractPaymentHandler` | `07` | `15` recurring, `16` separate frontend, `18` cart coupling, `24` external-API caching |
| `cart`, `checkout`, `line item`, `delivery`, `promotion`, `CartBehavior` | `18` | `04` backend, `07` payment, `13` pricing scope, `24` external-API caching |
| `Twig`, `storefront`, `theme`, `SCSS`, `storefront JS`, `activeRoute`, `ESI` | `05` | `17` accessibility, `16` separate frontend, `21` snippets |
| `cache`, `http cache`, `varnish`, `reverse proxy`, `cache invalidation`, `sw-cache-hash` | `23` | `04`, `05`, `11` for backend/storefront/ops overlap, `10` for exact docs/anchors |
| `admin`, `app`, `cloud`, `manifest`, `Meteor`, `mt-`, `Pinia`, `Vite`, `MCP server` | `06` | `02` migration/version split, `21` snippets |
| `queue`, `messenger`, `rabbitmq`, `worker`, `async`, `webhook transport` | `04`, `11`, `14` | `18` checkout handoff, `20` indexer workers |
| `review`, `audit`, `analysis`, `code review`, `security review` | `08`, `22` | domain references matching touched flows |
| `test`, `PHPUnit`, `fixture`, `Store API test`, `SalesChannelApiTestBehaviour` | `19` | `18` cart, `07` payments, `20` indexing |
| `search`, `OpenSearch`, `Elasticsearch`, `listing`, `product search` | `20` | `04` DAL, `13` commerce scope |
| `indexer`, `reindex`, `dal:refresh:index`, `EntityIndexer` | `20` | `11` operations, `14` workers/commands |
| `snippet`, `translation`, `locale`, `i18n`, `messages.*.base.json`, `translation:install` | `21` | `05` storefront, `06` admin, `02` 6.7.3+ base snippets |
| `patch`, `composer-patches`, `PHPStan`, `php-cs-fixer`, `shopware-rector`, `Frosh Tools` | `25` | `11` for quality gates, `14` for CLI, `02` for backport policy |
| `external API in cart`, `TaxJar`, `Avalara`, `tax calculation cache`, `third-party cart data` | `24` | `18` pipeline, `04` DI, `11` operations |
| `CMS`, `Shopping Experiences`, `cms element`, `cms block`, `slot config`, `slotConfig`, `sw-cms`, `CmsElementResolver` | `27` | `05` storefront templates, `06` admin components, `23` rule-based visibility, `21` translated content |
| `shopware-cli project`, `project dev`, `compose.yaml`, `compose.override.yaml`, `docker compose exec`, `.shopware-project.yml`, `local environment`, `Mailpit`, `devenv`, `Lando` | `28` | `14` CLI, `20` OpenSearch, `11` operations, `21` DB snippet overrides |
| `plugin lifecycle`, `version bump`, `plugin:refresh`, `plugin:update`, `updateDestructive`, `custom field installer`, `didn't run after deploy` | `26` | `04` migrations, `12` custom fields, `02` version split |

Accessibility, ADA, WCAG, VPAT, screen reader, keyboard, form, focus, modal, storefront UX, or frontend audit tasks always read `05`, `10`, and `17`.

## Mode Workflow

| Mode | Do |
| --- | --- |
| Planning | Identify version, extension surface, hot path, source uncertainty, and 2-3 viable approaches when direction changes materially. |
| Implementation/refactor | Choose the extension point, make the smallest coherent safe change, preserve existing patterns, validate the narrowest useful surface. |
| Review/audit | Follow the 3-pass protocol in `22`, pin the baseline, scan the full affected flow, report findings first by severity and blast radius, separate actionable, deferred, inactive, and verification-gap items. |
| Research | Use docs plus matching source code. Prefer Markdown-source docs when doing detailed research. Cite exact docs or core anchors when behavior is version-sensitive. |
| PR/release summary | Use the detailed structure in `03`; use review output rules from `08` when writing findings. |

Before proposing or editing, inventory mutation surfaces, trust boundaries, ownership boundaries, browser-authored data, cross-plugin contracts, hot paths, and accessibility-sensitive UI patterns that apply.

## Cross-Cutting Rules

- Default to Shopware 6.7. Read 6.6 compatibility notes only when the project or request requires them.
- Prefer the smallest coherent safe change over the mechanically smallest diff. Apply DRY and KISS by default.
- Add safeguards only for concrete failure modes in the actual code path.
- Ask before choosing between valid approaches when the choice materially changes save behavior, persistence flow, entity modeling, native-component reuse, or admin/storefront UX.
- Protect cart, checkout, login, account, renewal, cache, queue, indexer, payment, and large admin-list hot paths.
- Never trust client-reported payment state, amount, provider references, ownership, or recurring authority.
- Never trust cart-token or context-token overrides from GET parameters when the target route mutates cart state. Use the `sw-context-token` header, not query strings, for token overrides on the same context.
- Cache every external-API call made during cart calculation with a TTL and a deterministic cache key. Never cache indefinitely. Expose a manual-invalidation admin route. Details in `24`.
- Keep controllers, subscribers, handlers, templates, and admin UIs thin. Move behavior into services or the owning extension point.
- Never assume the admin worker runs in production. Prefer CLI workers with explicit transports and failure queues.
- Never assume the default `shopware.usage_data.collection_enabled: true` is safe on large catalogs. Set it to `false` in YAML for production sites over ~50k products.
- Never edit `vendor/` directly. Use `cweagans/composer-patches` for vendor patches (details in `25`).
- A change that only runs from a plugin lifecycle hook needs a version bump to execute on already-installed shops. Fresh installs and tests never surface the gap. Details in `26`.
- Never put required work in `updateDestructive()`. Plugin install and update never call it.
- Validate after each chunk with the narrowest useful checks and report remaining risk.

## Reference Map

- [references/01-source-hierarchy.md](references/01-source-hierarchy.md) source order, core-source verification gate, ownership, repo-local overlays
- [references/02-version-targeting.md](references/02-version-targeting.md) 6.7 default, 6.6 compatibility, PHP/Symfony/Redis versions, backport policy
- [references/03-implementation-workflow.md](references/03-implementation-workflow.md) chunking, validation, PR/QA templates
- [references/04-plugin-backend.md](references/04-plugin-backend.md) backend, DAL, APIs, Messenger + webhook transport, migrations, FK conventions
- [references/05-storefront-and-themes.md](references/05-storefront-and-themes.md) Twig, JS, SCSS, themes, `activeRoute`, ESI header/footer, CSS custom props, event bus
- [references/06-administration-and-apps.md](references/06-administration-and-apps.md) admin modules, ACL, apps, Vue 3 + Pinia + Vite, `mt-*` components, MCP server
- [references/07-payments.md](references/07-payments.md) `AbstractPaymentHandler`, webhooks, saved methods, refunds, cart-vs-context token, middleware retry
- [references/08-analysis-and-reviews.md](references/08-analysis-and-reviews.md) review mode, severity, evidence, findings output
- [references/09-symfony-and-php.md](references/09-symfony-and-php.md) Symfony 7.3/7.4, PHP 8.4/8.5, named-argument constraints, `ResetInterface`
- [references/10-official-docs-map.md](references/10-official-docs-map.md) docs research protocol and source anchors
- [references/11-quality-and-operations.md](references/11-quality-and-operations.md) security, ops, observability, usage-data disable, store readiness, Frosh Tools
- [references/12-extension-patterns.md](references/12-extension-patterns.md) config, Flow Builder, CMS, custom fields XML, cookie event, Rule Builder
- [references/13-context-and-commerce.md](references/13-context-and-commerce.md) context, sales-channel scope, pricing, tax
- [references/14-cli-and-dev-tooling.md](references/14-cli-and-dev-tooling.md) console, workers, `shopware-cli` image, admin codemod, static analysis
- [references/15-subscriptions-and-recurring-payments.md](references/15-subscriptions-and-recurring-payments.md) subscriptions, renewals, saved-method ownership, middleware retry
- [references/16-headless-and-composable-frontends.md](references/16-headless-and-composable-frontends.md) composable frontend trust, Nitro/edge/backend cache separation, `context.token`
- [references/17-accessibility-and-template-best-practices.md](references/17-accessibility-and-template-best-practices.md) WCAG/EAA storefront review, `sw_icon` aria-hidden default, list semantics
- [references/18-cart-and-checkout-pipeline.md](references/18-cart-and-checkout-pipeline.md) collectors, processors, validators, `FilterableInterface`, `SKIP_CART_PERSISTENCE`
- [references/19-testing-patterns.md](references/19-testing-patterns.md) integration tests, Store API tests, fixtures, mocks, migrations
- [references/20-search-and-indexing.md](references/20-search-and-indexing.md) search, indexers, `/api/_action/indexing` `only`, ES env vars, admin ES
- [references/21-internationalization-and-snippets.md](references/21-internationalization-and-snippets.md) snippets, translations, country-agnostic base files, Language Pack sunset
- [references/22-code-review-protocol.md](references/22-code-review-protocol.md) 3-pass review protocol, report format, finding rules
- [references/23-cache-and-http-cache.md](references/23-cache-and-http-cache.md) delayed invalidation, CACHE_REWORK, `sw-cache-hash`, Varnish/Fastly integration
- [references/24-external-api-caching-in-cart.md](references/24-external-api-caching-in-cart.md) TaxJar-style caching contract, TTL, cache-key components, admin invalidation
- [references/25-patching-and-dependency-tooling.md](references/25-patching-and-dependency-tooling.md) composer-patches, PHPStan/PHPCS pinning, shopware-rector, Frosh Tools, mysqldump
- [references/26-plugin-lifecycle-and-activation.md](references/26-plugin-lifecycle-and-activation.md) lifecycle methods, version bump chain, what needs a bump to deploy, `updateDestructive`
- [references/27-cms-elements-and-blocks.md](references/27-cms-elements-and-blocks.md) slot config storage and override merge, `sw-cms-inherit-wrapper`, admin registration and previews, custom page types, resolvers, rule-based visibility, translating CMS content
- [references/28-local-dev-environment.md](references/28-local-dev-environment.md) `shopware-cli project dev`, generated `compose.yaml` and overrides, running commands in `web`, cheapest rebuilds, queue/scheduler/OpenSearch locally, mail safety with production dumps, testing pitfalls, devenv/Lando migration

## It's Working If

- The skill appears in `/skills` (Claude Code) or Codex skill listing after install.
- The skill auto-invokes when the user types "review my Shopware plugin", "fix Shopware cache invalidation", or any phrase from `when_to_use`.
- On a review task, the assistant reads `references/08-analysis-and-reviews.md` and `references/22-code-review-protocol.md` before writing findings.
- On a cache-invalidation question, the assistant reads `references/23-cache-and-http-cache.md` before answering.
- On an external-API-in-cart question, the assistant reads `references/24-external-api-caching-in-cart.md` and mentions TTL, cache key components, and manual-invalidation route.
- On a payment task, the assistant references `AbstractPaymentHandler`, `pay/finalize/validate/recurring/refund`, and the `shopware.payment.method` DI tag from `references/07-payments.md`.

## Anti-Patterns To Avoid

- Do not include time-sensitive language like "as of 2026" in guidance. State versions with SemVer instead.
- Do not offer multiple approaches when one is clearly correct. Encode opinion; explain trade-off only when the choice is genuinely open.
- Do not assume a plugin has `Frosh Tools`, Redis, or Varnish installed. Detect first, then suggest.
- Do not add rules without a matching Shopware release note, ADR, or documented community pattern.
- Do not pre-approve bare `Bash` in `allowed-tools`. Use specific patterns like `Bash(git status *)`.
- Do not expose `context.token` in Twig or logs. It is a security boundary.
- Do not confuse `cluster_setup` (Symfony cache clustering) with HTTP cache. They are separate systems.
