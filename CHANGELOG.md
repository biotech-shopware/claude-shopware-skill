# Changelog

All notable changes to the universal Shopware AI skill are documented in this file.

## [v0.8.0-dev] - 2026-08-21 (dev branch)

This entry documents the `dev` branch. It is not merged to `main` yet. Install v0.7.3 from `main` for production; install this from `dev` to preview.

### Frontmatter

- Rewrote `description` in third person with literal user paraphrases in the first 200 characters ("review my Shopware plugin", "fix Shopware cache invalidation", "add a payment handler", etc.). Community best practice: descriptions match on paraphrase, not feature catalogs. (Anthropic docs `description` field guidance; DEV rulestack `skillmd-that-actually-triggers`.)
- Added `when_to_use` frontmatter field with trigger phrases users actually type. Anthropic appends this to `description` for auto-invocation matching. Combined length kept under the 1,536-char truncation cap.
- Added `paths` frontmatter with Shopware-scoped globs (`composer.json`, `custom/**`, `src/**/*.php`, `src/**/*.twig`, `**/theme.json`, `**/manifest.xml`, etc.) so the skill auto-invokes on Shopware repos and stays quiet in unrelated projects.
- Expanded `allowed-tools` from `Read, Glob, Grep` to include `Edit`, `Write`, and specific `Bash(...)` patterns for common Shopware read-only console commands (`bin/console debug:* *`, `bin/console cache:watch:delayed *`, `bin/console messenger:stats *`, etc.). Least-privilege pattern per Lee Han Chung's Claude Skills deep dive.
- Added `argument-hint: "[plan|implement|review|audit|research] <task description>"` for autocomplete UX.

### SKILL.md body

- Added explicit Read-tool hint above the routing matrix: "When the routing matrix points to a number like `07`, open `references/07-payments.md` with the Read tool before starting the task."
- Extended the routing matrix with `23` (cache/HTTP cache), `24` (external-API-in-cart caching), and `25` (patching/dependency tooling); added file `22` (code review protocol) to the review/audit row.
- Expanded the accessibility trigger row to also mention `05`, `10`, `17` for ADA/VPAT/keyboard/screen-reader/modal tasks.
- Updated Mode Workflow's Review/audit row to explicitly reference the 3-pass protocol in `22`.
- Added Cross-Cutting Rules for cart-token vs context-token separation (never accept cart-token overrides via GET query strings), external-API cache contract in cart, `shopware.usage_data.collection_enabled: false` on large catalogs, and never editing `vendor/` directly (use `composer-patches`).
- Added "It's Working If…" observable-success section for install verification (Matt Pocock skills pattern).
- Added "Anti-Patterns To Avoid" section: no time-sensitive language, no offering multiple approaches without reason, no assumption of Frosh Tools / Redis / Varnish installed, no bare `Bash` in `allowed-tools`, no `context.token` in Twig or logs, no confusion between `cluster_setup` and HTTP cache.
- Reference Map extended to list all 25 references with a one-line description per file (was: 21 files, terse).

### New reference files

- `references/22-code-review-protocol.md` — verbatim 3-pass review protocol (setup, scope, passes, findings shape, prior-review handling, rules). Codified from a battle-tested review prompt.
- `references/23-cache-and-http-cache.md` — delayed cache invalidation defaults per version (6.6=20s, 6.7=5min with `cache_rework`), `sw-cache-hash` narrowed to price-relevant rules, `CACHE_REWORK` flag (renamed from `CACHE_CONTEXT_HASH_RULES_OPTIMIZATION` in 6.7.5), removed `Cached*Route` classes, deprecated cache state symbols, ESI header/footer, external Varnish/Fastly integration, `NavigationRoute` cache-key event, invalidation-cost warnings from real production data. Sources: release notes 6.7.0/6.7.5/6.7.6/6.7.11, UPGRADE-6.7.md, Rune Laenen Slack threads Aug 2026.
- `references/24-external-api-caching-in-cart.md` — TaxJar-style caching contract for any plugin calling an external API from a `CartDataCollector` / `CartProcessor`. Cache key components, TTL rules (8 hours default for tax/shipping providers), admin invalidation route pattern, live-check on order placement, extendability requirements, provider-side auto-invalidation ideal case, review prompts. Source: real-world TaxJar plugin review thread Aug 2026.
- `references/25-patching-and-dependency-tooling.md` — `cweagans/composer-patches` for vendor patches, backport policy for 6.6 fixes only in 6.7, PHPStan/PHPCS pinning (1.12.5/3.64.0) with `--memory-limit=2G`, `FriendsOfShopware/shopware-rector` set list `SHOPWARE_6_7_0` with specific rectors, `FriendsOfShopware/FroshTools` for in-admin observability with 6.6 counter caveats, canonical `mysqldump` with `--single-transaction --routines --hex-blob` and `DEFINER=` stripping, security audit workflow, `auth.json` guidance. Sources: laenen.me blog posts, FriendsOfShopware GitHub, Rune Slack Aug 2026.

### Existing reference file updates

- `references/01-source-hierarchy.md` — added ownership bullets for files 22, 23, 24, 25.
- `references/02-version-targeting.md` — added runtime version matrix (PHP 8.4 default, 8.5 supported 6.7.6+, Symfony 7.3 baseline 6.7.2, Symfony 7.4 from 6.7.7, `php-redis` 6.1+ from 6.7.7, MySQL settings), Language Pack sunset in 6.8 with `translation:install --locales`, backport policy note (not all 6.7 fixes backport to 6.6; example PR #18205 6.7.13.0+ only; use composer-patches).
- `references/04-plugin-backend.md` — added FK naming change `fk__table__col` and `TableHelper`, custom field snake_case rule, `EntityDefinition::__construct` deprecation, `ScheduledTaskHandler` `LoggerInterface` requirement, messenger message size cap `shopware.messenger.message_max_kib_size`, `WEBHOOKS_REWORK` transport with retry ladder, `NavigationRoute` `CategoryLevelLoaderCacheKeyEvent` subscription, Sync API foreign-key resolvers (technical names/ISO codes), state machine per-entity locking, Store-API `limit` cap, `ResetInterface` for FrankenPHP/RoadRunner, product `states` → `type` model, sales channel repository default from Rune Slack.
- `references/05-storefront-and-themes.md` — added `controllerName`/`controllerAction` → `activeRoute` (Twig/JS/CSS), cookie provider replaced by `CookieGroupCollectEvent`, global storefront event bus `window.Shopware.emit`/`on` + `PluginManager.callPluginMethod` (6.7.11), Vite dev server `composer storefront:dev-server` (6.7.11), theme config auto-exposed as CSS custom properties `var(--sw-*)`, `theme.json` per-file references `@BundleName/…`, `context.token` removed from Twig (`GHSA-6w82-v552-wjw2`), ESI header/footer routes with detailed extension pattern, `sw_breadcrumb_full*` requires `SalesChannelContext`, EAA-driven markup baseline (1rem font-size, `sw_icon` aria-hidden default, `<ul>`/`<li>` line items).
- `references/06-administration-and-apps.md` — added Vite + Pinia + Vue 3 details (async components by default, `@vue:mounted` for refs, `mapVuexState` legacy vs `mapState` Pinia, `$tc` shimmed), full Meteor components mapping table (`sw-button` → `mt-button`, 20 renames), admin codemod command with `-v 6.7`, `sw-entity-listing` `items` → `dataSource`, rule builder condition contract updates (`LineItemProductStatesRule` → `LineItemProductTypeRule`, `LineItemPurchasePriceRule` type change, `sw-condition-generic` replaces specific components, `sw-condition-field-errors`), filesystem `visibility` top-level, OAuth `scope` string not array + `/api/oauth/authorize` removal, MCP server integration (`/api/_mcp`, `mcp.tool`/`mcp.prompt`/`mcp.resource` tags, `debug:mcp` CLI, `MCP_SERVER` flag removed 6.7.14), payment/shipping `technicalName` non-nullable warning with `temporary_<id>` auto-migration risk.
- `references/07-payments.md` — added `AbstractPaymentHandler` consolidation (5 legacy interfaces deprecated, `pay/finalize/validate/recurring/refund` + `supports()`), `shopware.payment.method` single DI tag, handler receives only `orderTransactionId` + request + `Context`, `technicalName` discipline with plugin prefix, SwagPayPal 6.7 reference architecture (single abstract + per-method subclasses, three lifecycle methods), Order `primaryOrderTransaction` field, cart-token vs context-token pitfall section, middleware retry = duplicate orders section, external API in cart cross-reference to `24`.
- `references/09-symfony-and-php.md` — added Symfony 7.3/7.4 versions and PHP 8.4/8.5 baseline, `php-redis` 6.1+, named-argument constraint constructors (Symfony 7.4), `ResetInterface` implementation for FrankenPHP/RoadRunner compat.
- `references/11-quality-and-operations.md` — added `shopware.usage_data.collection_enabled: false` on large catalogs with observed `UsageData EntitySync` writer-replica CPU domination, `shopware.messenger.message_max_kib_size` details, `maintenanceIpWhitelist` → `maintenanceIpAllowlist` rename, `SHOPWARE_SKIP_WEBINSTALLER` for read-only FS, Elasticsearch env vars (`SHOPWARE_ES_THROW_EXCEPTION=1`, `SHOPWARE_ES_USE_LANGUAGE_ANALYZER`, `SHOPWARE_ADMIN_ES_ENABLED`, `ENABLE_OPENSEARCH_FOR_ADMIN_API`), performance baseline (Redis for delayed invalidation, opcache config, zstd, `.env.local.php`), FroshTools observability with 6.6 counter caveat, static analysis pinning (PHPStan 1.12.5, php-cs-fixer 3.64.0), MySQL dump canonical form.
- `references/12-extension-patterns.md` — added custom fields in `Resources/config/custom-fields.xml` with `<include-in-search>true</include-in-search>` and `Immutable` flag (6.7.7, 6.7.13), cookie provider replaced by `CookieGroupCollectEvent` + Store-API route `/store-api/cookie-groups`, rule builder condition contract shifts.
- `references/14-cli-and-dev-tooling.md` — added `composer storefront:dev-server` (6.7.11), `bin/console sales-channel:replace:url`, `bin/console cache:watch:delayed` + `cache:clear:delayed`, webhook transport consumer (`messenger:consume webhook async low_priority`), translation CLI (`translation:validate`, `translation:list`, `translation:install --locales`), admin codemod, `shopware-cli` Docker image, Rector and Frosh Tools pointers.
- `references/15-subscriptions-and-recurring-payments.md` — added `AbstractPaymentHandler::recurring()` and `supports()` capability check, middleware retry loops cause duplicate renewals section.
- `references/16-headless-and-composable-frontends.md` — added `context.token` removed from Twig (security), three cache layers (Nitro / edge / Shopware backend) explanation, middleware retry = duplicate orders section, WebScale/Fastly/Varnish hook Shopware cache-tag system.
- `references/17-accessibility-and-template-best-practices.md` — added 6.7 storefront accessibility baseline (1rem font-size, `sw_icon` `aria-hidden` default with opt-out, semantic button/link switch, `<ul>`/`<li>` line items, product-card duplicate-link removal, modal-trigger button pattern, `-Modal` snippet key variants), theme snippet keys required in 6.8 (constructed key pattern, `labelSnippetKey`/`helpTextSnippetKey`, `ThemeConfigurationService::getPlainThemeConfiguration()`).
- `references/18-cart-and-checkout-pipeline.md` — added `CartBehavior::isRecalculation` deprecation → `CheckoutPermissions` + `SKIP_CART_PERSISTENCE` + `CartVerifyPersistEvent`, `FilterableInterface` required for filtered price definitions with `getFilter()`, Order `primaryOrderDelivery`/`primaryOrderTransaction`, product `states` → `type` model with `shopware.product.allowed_types`, cart-token vs context-token pitfall, external API in cart cross-reference to `24`.
- `references/20-search-and-indexing.md` — added `POST /api/_action/indexing` with `{"only": ["category.indexer"]}` undocumented reindexing endpoint (returns 204, queued), Elasticsearch env vars, FroshTools queue endpoint `/api/_action/frosh-tools/queue/list` with 6.6 counter caveat.
- `references/21-internationalization-and-snippets.md` — added country-agnostic base snippet layer (6.7.3+, `en.json` not `en-GB.json`, `messages.en.base.json` not `messages.en-GB.base.json`, 4-step resolution order, ~70 delta snippets vs ~12,000 duplicates), snippet CLI (`translation:validate`/`list`/`install --locales`), Language Pack sunset in 6.8 with FK-constraint upgrade path, theme snippet keys required in 6.8 with constructed pattern.

### Distribution

- Added `.claude-plugin/plugin.json` manifest so users can install as a Claude Code plugin. Includes name, version `0.8.0-dev`, description, author, homepage, repository, license, keywords, and skill path.
- Added `eval/should-trigger.md` with 30 prompts to test auto-invocation across plugin work, payments, cart, cache, storefront, admin, i18n, and ops. Target hit rate ≥ 4/5.
- Added `eval/should-not-trigger.md` with 18 prompts (generic PHP/Symfony, other e-commerce platforms, unrelated topics, adjacent-but-not-Shopware) to bound false-positive rate ≤ 1/5.
- Added `docs/verify-install.md` with 5-step install verification checklist (file presence, `/skills` listing, auto-invocation, reference-open behavior, reference-specific dry runs).
- Updated `agents/openai.yaml` `short_description` to include "code review protocol", "cache/HTTP cache", "delayed invalidation", "external-API caching in cart", "AbstractPaymentHandler", "composer-patches", "shopware-rector", "Frosh Tools" so Codex users match on those keywords too.

### Codex compatibility

- `agents/openai.yaml` retained. All `references/NN-topic.md` paths remain relative.
- No `context: fork` or Claude-Code-only frontmatter fields added to the main `SKILL.md` (frontmatter uses only fields that either exist in both runtimes or are ignored by Codex without error).
- New reference files are plain markdown, loadable by both Codex and Claude Code readers.

### Validated

- Frontmatter parses as valid YAML (name, description as `>-`, `when_to_use` as `>-`, `paths` as list, `allowed-tools` as list, `argument-hint`).
- Reference file count: 25 (was 21 in v0.7.3).
- Every added rule is cited to a Shopware release note, ADR, developer.shopware.com doc, Rune Laenen blog post, or a specific Rune Slack thread.
- Rune's actual Slack channels are `#altus-nova_shopware` and `#webscale-shopware-altusnova` (no `nu-tech` channel exists — search returned empty).

### Sources cited

- Shopware release notes 6.7.0 through 6.7.13 on developer.shopware.com/release-notes/6.7.
- `UPGRADE-6.7.md` on github.com/shopware/shopware.
- Rune Laenen laenen.me blog posts on PHPStan setup, composer-patches, mysqldump.
- Rune Laenen Slack messages Aug 2026 (`#altus-nova_shopware`, `#webscale-shopware-altusnova`, DMs).
- FriendsOfShopware GitHub org (FroshTools, shopware-rector).
- SwagPayPal 6.7 refactor announcement on shopware.com/en/news.
- developer.shopware.com performance tweaks, cart processor/collector, Store API add-route, Meteor components, Language Pack migration, country-agnostic-language-layer ADR.
- Anthropic official skill docs (code.claude.com/docs/en/skills.md, platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- Community skill-authoring posts: Matt Pocock, Simon Willison, Anthropic plugin-dev SKILL.md, DEV, MindStudio, vanja.io, paddo.dev, Response Awareness, Acydoan, William Spurlock, Shiqi Mei, Lee Han Chung.

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
