# Shopware 6 Code Review Guidelines

Apply these criteria to Shopware 6 plugin, project, Administration, and classic storefront changes. Report only issues supported by the changed code and its affected flow. Do not turn every guideline into a comment.

## Review Baseline and Evidence

- Resolve the Shopware version from root and extension `composer.json`, installed package metadata, or a targeted lock-file lookup. Default to Shopware 6.7 only when the project does not establish another supported version; apply 6.6 compatibility rules when required.
- Verify behavior-sensitive claims and named core classes, services, routes, events, feature flags, Twig blocks, Administration components, commands, and storefront imports against installed `vendor/shopware/*` code or the matching stable Shopware core tag. Source behavior wins when documentation or examples disagree.
- Review the complete affected flow, not only the changed function. Follow controllers, routes, services, subscribers, DAL definitions, migrations, handlers, templates, JavaScript, configuration, queues, and tests that participate in the behavior.
- Pin findings to the reviewed commit or working-tree state. Treat code that changed between reviews as a changed baseline.
- Distinguish confirmed defects from hypotheses, inactive or dormant code, deferred scope, third-party limitations, and runtime verification gaps.
- Require an exact file and symbol, realistic failure mode, affected users or systems, production blast radius, smallest coherent safe fix, regression risk, and practical validation for each material finding.
- Use P0 for exploitable security/payment trust failures, broken idempotency, cache collapse, or severe hot-path regressions; P1 for broad correctness, migration, performance, or operational failures; P2 for material maintainability, compatibility, or testing gaps.
- Avoid speculative defensive recommendations. A safeguard must address a concrete failure mode in the reviewed path.
- If no material issue is present, report no finding rather than manufacturing style feedback.

## Architecture and Change Shape

- Verify the change uses the owning Shopware extension point instead of bypassing it with copied core logic, direct container access, internal HTTP calls, or fragile inheritance.
- Prefer the smallest coherent safe change, not the mechanically smallest diff. Flag duplicated helpers or services when widening one existing seam would keep behavior DRY and simpler.
- Keep controllers, Store API/Admin API routes, subscribers, message handlers, scheduled tasks, Twig templates, and Administration components thin. Domain rules and orchestration belong in testable services or the responsible processor, validator, resolver, loader, or handler.
- Use constructor injection. Treat runtime service-locator calls and static global state as architectural regressions unless the framework contract requires them.
- Prefer decoration and supported events over replacing core services or copying core implementations. Verify decorators preserve the decorated contract and call the inner service where required.
- Preserve existing project conventions when they are intentional and safe. Do not demand a broad rewrite solely to match a generic pattern.
- Verify external integrations are behind one adapter that owns authentication, timeouts, retries, redaction, error translation, and observability.
- Flag plugin install, update, activate, or uninstall hooks that perform unreliable remote provisioning or unrelated business work. Lifecycle code must be repeatable and limited to lifecycle concerns.

## DAL, Entities, Migrations, and Backend APIs

- Use DAL for normal entity behavior. Require bound parameters for necessary DBAL or raw SQL and verify the query preserves Shopware versioning, translation, inheritance, and context semantics where applicable.
- Verify repository reads are bounded and load only required fields and associations. Flag `search()` calls inside loops, unbounded criteria, deep association graphs, full cart/order blob hydration, and list endpoints without pagination.
- Prefer `searchIds()` when only identifiers are needed. Batch reads and writes instead of issuing one query per entity or line item.
- Treat custom fields as merchant-managed metadata. Prefer an entity extension for structured fields attached to an existing entity and a custom entity for operational state, deduplication, sync history, lifecycle state, or independently queried records.
- Verify custom-field updates merge existing values unless full replacement is explicit. Do not use mutable JSON/custom-field blobs as primary query or deduplication state at scale.
- Avoid redundant casts, trims, null fallbacks, or validation after a typed DAL/config contract already guarantees the value. Keep normalization only at real untrusted-input boundaries.
- Keep migrations immutable after release. Require a new migration instead of editing an executed one, idempotent schema operations where practical, destructive work in `updateDestructive()`, and indexes matching actual filters, joins, uniqueness, and sorting.
- Keep large backfills out of synchronous migration execution. Require bounded, resumable processing before final constraints or indexes depend on migrated data.
- Verify state changes use Shopware state-machine transitions or the owning transition service rather than direct technical-state writes.
- Admin API routes require ACL and narrow privileges. Customer-facing Store API/storefront mutations require authentication where applicable, ownership checks, bounded payloads, and non-GET methods.
- Verify storefront code never calls privileged Admin API routes directly and backend code does not call its own shop through HTTP when the underlying service can be injected.
- Check every temporary upload or generated file for cleanup on success, validation failure, exception, and retry paths.

## Shopware Extension Surfaces

- Keep merchant settings in `config.xml` behind a typed configuration service. Read sales-channel-specific values through normal inheritance, validate real external input, and keep shop-specific secrets out of code and logs.
- Emit one explicit business or Flow Builder-compatible event after the owning state is committed when merchants should configure mail, tags, webhooks, or other reactions. Do not duplicate those side effects across state subscribers.
- A CMS element or block must align Administration registration, storefront template, resolver, and data struct. Collect IDs/data in `collect()`, attach prepared data in `enrich()`, and keep Twig free of repository calls.
- Prefer Shopware import/export profiles, field mappings, serializers, and converters over ad hoc CSV controller loops. Large imports must be chunked, resumable, observable, and explicit about translations, media, nested fields, prices, tax, and custom fields.
- Use Shopware media entities, folders, media services, and file savers rather than writing public files directly. Validate remote sources, apply SSRF controls, configure thumbnails deliberately, and remove temporary files on every exit path.
- Use custom Rule Builder rules for merchant-configurable pricing, shipping, promotion, or content conditions. Verify the correct rule scope, typed operators, deterministic payload access, and `RuleConfig` Administration configuration.
- Give plugin-owned discounts, credits, fees, and bundles a registered technical line-item type. Never drive business behavior from translated labels or a reused generic type.
- Keep transactional-mail ownership in Flow Builder, one business event, or one orchestration service. Extend mail templates and payloads through stable hooks and queue delivery when the hot path does not require synchronous completion.
- Keep product variants, properties, product streams, and cross-selling aligned with Shopware catalog models. Use custom fields for editorial metadata and structured/custom entities for operational or independently queried catalog state.

## Storefront, Twig, JavaScript, SCSS, and Themes

- Extend the smallest stable Twig block and preserve upstream markup, accessibility, data attributes, plugin selectors, and extension points. Flag full core-template copies unless no safe block-level extension exists.
- Verify the target template path and block exist in the project version. Do not accept guessed block names or storefront-only Twig functions in Administration templates.
- Keep data loading in page loaders, CMS resolvers, Store API routes, controllers, or services. Flag DAL queries, `searchMedia()`, expensive filters, remote calls, or writes from Twig and repeated rendering loops.
- Escape dynamic text and attributes by default. Allow raw HTML only from an explicitly trusted and sanitized source.
- Keep repeated component IDs unique and derive related `for`, `aria-controls`, `aria-describedby`, and target attributes from the same stable suffix.
- Scope storefront plugins to their component root. Flag broad `document.querySelector`, body-wide mutation observers, unbounded polling, duplicate initialization, and event listeners or timers that are not removed on teardown.
- Use existing Shopware plugin/component behavior before adding inline scripts or parallel custom frameworks. Verify async initialization, global events, and Vite behavior against the installed 6.7 minor.
- Keep SCSS selectors component-scoped and avoid broad overrides or deprecated patterns that copy or tightly couple to core internals.
- Verify third-party scripts and widgets are consent-aware, loaded once, failure-tolerant, and do not block rendering or checkout.
- Protect SEO output: canonical URLs, metadata, structured data, hreflang, robots behavior, and semantic heading structure must remain coherent after overrides.

## Administration

- Verify Shopware 6.7 Administration changes are Vue 3, Pinia, and Vite compatible; do not reuse Vue 2 lifecycle, filter, private component, or build assumptions without an explicit 6.6 branch.
- Prefer supported module, component-extension, override, data-repository, and ACL patterns. Verify the actual component/template blocks against the target core version.
- Require every privileged action to be protected in both UI visibility and backend ACL. Hiding a button is not authorization.
- If plugin-owned data conceptually belongs to a parent entity edit screen, prefer the normal parent save flow. Flag immediate writes from tabs, assignment editors, or click handlers when they cause chatty persistence, partial state, or inconsistent cancellation behavior without a documented reason.
- Keep list loading paginated and criteria bounded. Avoid loading full associations or one request per row.
- Verify loading, empty, error, retry, unsaved-change, and permission-denied states. External diagnostics actions must return actionable, redacted errors.
- Administration Twig templates are automatically extended; flag explicit storefront-style `extends`/`sw_extends` use or storefront-only functions.

## Cart, Checkout, Delivery, and Promotions

- Preserve the cart lifecycle: collectors fetch or precompute data into `CartDataCollection`, processors mutate the calculated cart from prepared data, and validators add actionable errors without hidden I/O or side effects.
- Verify collector data is keyed by stable identifiers and fetched once in batches. Flag repository or remote API calls repeated in processors, validators, or per-line-item loops.
- Treat processor priority and recalculation order as correctness boundaries. Check interactions with product pricing, custom fees, promotions, free-shipping thresholds, tax, and delivery calculation.
- Use `LineItemFactoryRegistry` and registered line-item types. Validate browser-provided referenced IDs and whitelist payload fields; keep line-item payloads small and deterministic.
- Validators must be cheap, deterministic, and scoped to the exact line item or checkout condition. They must not widen ownership or trust browser-authored customer, payment, shipping, or recurring identifiers.
- Recalculate from the current `SalesChannelContext` when currency, tax, shipping, payment availability, rules, or customer state may have changed. Do not patch totals manually from stale snapshots.
- Keep correctness-critical totals and availability synchronous. Move post-order ERP, CRM, reporting, and notification side effects to queues only after the order and transaction intent are durably persisted.
- External shipping or tax calls on checkout require strict timeouts, bounded payloads, safe caching keyed by all relevant cart/address/context dimensions, and an explicit failure path. Do not cache one quote across incompatible carts or addresses.
- Verify shipping logic uses the shipping address and correct delivery context rather than silently substituting billing data.
- Flag writes or expensive recalculation hidden in cart, confirm, offcanvas, or other read-only page loads.

## Payments and Webhooks

- Derive payable amount, currency, customer, order, transaction, and success state from server-side Shopware/provider data. Browser fields, redirects, hidden inputs, query parameters, local storage, and client telemetry are not payment authority.
- Verify the implementation matches the exact target payment-handler contract. Shopware 6.7 uses `AbstractPaymentHandler`; Shopware 6.6 compatibility may involve deprecated interfaces and must be checked against installed core.
- Keep `validate()` fast and deterministic, `pay()` explicit about redirect versus synchronous outcomes, and `finalize()` idempotent and bound to the correct transaction.
- Persist provider operations with stable idempotency keys and explicit intent/state before or atomically with money movement where possible. A retry must not create a second charge, capture, refund, void, or order.
- Model unknown provider outcomes explicitly. A timeout after submission is not proof of failure and must trigger reconciliation rather than blind replay.
- Verify webhook signatures over the exact raw body and provider canonicalization, use constant-time comparison where applicable, reject missing/invalid signatures before parsing effects, and defend against replay.
- Webhook handlers must correlate provider references to the exact Shopware transaction, be idempotent, and apply valid state transitions. Keep webhook management behind Administration ACL; the public callback remains narrowly authenticated server-to-server input.
- Build callback and return URLs from trusted sales-channel domains or explicit configuration, not request host headers or browser-supplied URLs.
- Saved-method display, use, replacement, and deletion require authenticated customer ownership and provider/customer correlation. A raw vault/card ID is never sufficient authorization.
- Refund, capture, and void operations must validate transaction ownership, amount/currency limits, prior operation state, and provider support before changing local state.
- Redact API keys, signatures, tokens, card data, provider payloads, context tokens, and personal data from logs and browser output.

## Subscriptions and Recurring Commerce

- Customer-facing cancel, pause, reactivate, skip, schedule, or payment-method changes require authentication, ownership, bounded input, and non-GET mutation routes.
- Scope subscription reads and mutations by current customer and relevant sales channel; do not load by raw UUID alone.
- Treat subscription lifecycle, recurring order creation, payment operation, and provider state as separate but correlated authorities. Verify the owner of each transition across participating plugins.
- Rebuild recurring carts/orders through the real sales-channel calculation path. Re-evaluate prices, tax, currency, shipping, rules, product availability, and payment eligibility rather than copying stale totals.
- Use stable renewal and payment idempotency keys. Retries, overlapping workers, webhooks, and manual recovery must not create duplicate orders or charges.
- Verify saved-method replacement is atomic with the subscription choice or has a recoverable intermediate state. Deleting a method must not silently orphan future renewals.
- Signed provider events or server-side provider verification must precede successful recurring payment state. Bind every callback/finalize event to the correct renewal and transaction.
- Keep snapshots minimal, redact sensitive fields, bound retention, and avoid loading large snapshots across recurring batches unless required.

## HTTP Cache and Varnish

- Verify only genuinely public read routes opt into `_httpCache`. Personalized, session-mutating, write, authorization, and sensitive endpoints must not be cached as shared responses.
- Preserve Shopware cache variation and invalidation behavior. Check `sw-cache-hash`, invalidation states, cache tags, route policies, and the exact 6.7 feature/config behavior against installed core.
- Flag customer-specific markup rendered into anonymous cacheable HTML. Isolate personalization behind a safe dynamic request or non-cacheable fragment instead of disabling cache for the whole page.
- Treat new cookies, sessions, response headers, redirects, and request-dependent values on cacheable storefront routes as cache-key and hit-rate changes requiring evidence.
- Keep invalidation narrow and tied to real data dependencies. Flag broad invalidation on high-frequency writes and plugin-specific invalidation that duplicates authoritative core Store API/page-loader tags.
- Verify Varnish behavior for anonymous, cart-filled, and logged-in states and after relevant entity updates. A local application-cache test alone is insufficient for reverse-proxy-sensitive changes.

## Messenger, RabbitMQ, Scheduled Work, and Operations

- Queue non-interactive side effects, but keep correctness-critical cart, checkout, authorization, and immediate state decisions on the request path when the user cannot proceed without them.
- Messages should contain stable IDs and minimal immutable context, not entities, requests, credentials, or large payloads. Handlers re-read current authoritative state.
- Handlers must be idempotent, bounded, retry-safe, and observable. Configure retry limits/backoff, a failure transport, operator recovery, and separate low-priority traffic when backlog could starve checkout-sensitive work.
- Use CLI workers in production and consume intended transports explicitly. Treat the browser-driven Administration worker as a development convenience, not the production topology.
- Do not recommend Symfony `DelayStamp` as a portable Shopware default because it is incompatible with some supported Messenger transports. Prefer scheduled tasks or persisted due-time processing unless the project proves transport-specific delay support.
- Scheduled tasks need realistic intervals, bounded batches, safe overlap behavior, technical identifiers, and success-aware schedule advancement. Avoid full-table scans and large association hydration.
- Console commands should be orchestration-only, delegate to services, bound expensive work with IDs/limits/time ranges, support `--dry-run` where mutation risk warrants it, and confirm unexpectedly broad runs.
- Flag controllers or services that launch the project's own console commands through `Process`; invoke the service directly or hand work to Messenger/scheduled tasks.
- Verify external calls use shared clients, TLS verification, explicit connect/response timeouts, retries only for safe/idempotent operations, and circuit-breaker or fallback behavior where outages can affect the shop.
- Use structured, redacted logs with correlation and operation IDs. Bound audit/snapshot retention and avoid application tables becoming unbounded log sinks.
- Treat queue backlog, failed-message growth, cache hit rate, invalidation frequency, indexer pressure, DB query count, and external latency as rollout risks.

## Search and Indexing

- Use Shopware search/listing routes and configured search abstractions for storefront search. Do not replace them with raw DAL/SQL search that bypasses language, visibility, sales-channel, scoring, or OpenSearch behavior.
- Treat index mapping, data fetch, and query behavior as one contract. A new indexed field requires compatible mapping, population, language/visibility semantics, query use where intended, and a reindex plan.
- Prefer existing write events when incremental recomputation is enough. Add an `EntityIndexer` only for data that needs full rebuild and queued incremental indexing.
- A custom `EntityIndexer` must implement `getName()`, bounded `iterate(?array $offset)`, targeted `update(EntityWrittenContainerEvent)`, idempotent `handle(EntityIndexingMessage)`, `getTotal()`, and `getDecorated()`; register it with `shopware.entity_indexer`.
- Use `IteratorFactory` for bounded full-index batches. `update()` emits only affected IDs and preserves the write context; `handle()` validates/deduplicates IDs and reads current state.
- Prevent recursive indexing deliberately when `handle()` writes through DAL. Keep indexer messages small and workers isolated when index work could block higher-priority traffic.
- Mapping changes require an explicit `dal:refresh:index` or equivalent rollout strategy. Verify rebuild duration, queue growth, DB load, index size, and MySQL/OpenSearch fallback behavior.
- Verify search-dependent writes, emitted messages, worker handling, index population, and returned results align end to end.

## Testing and Release Validation

- Choose the narrowest test that proves behavior: unit tests for pure services, Shopware integration tests for DAL/wiring/migrations, request-level tests for Store API/storefront routes, and browser/E2E tests for runtime Administration, storefront, cache, or accessibility behavior.
- Use Shopware test traits such as `IntegrationTestBehaviour`, `KernelTestBehaviour`, and `SalesChannelApiTestBehaviour` according to the required boundary. Avoid ad hoc kernel bootstrapping and shared persistent fixtures.
- Product, customer, order, and payment fixtures must satisfy real entity requirements. Prefer verified Shopware fixture helpers or explicit complete payloads.
- Configure `StaticEntityRepository` with the actual result type consumed by the test, such as an entity collection, `EntitySearchResult`, `IdSearchResult`, or callable. Ensure queued results match call order.
- Cover success, rejection, ownership failure, retry, duplicate delivery, degraded provider, and relevant 6.6/6.7 compatibility paths for high-risk changes.
- Require container boot/compile validation after service, decorator, handler, scheduled-task, or DI changes and migration tests when schema/backfill risk is material.
- Validate cache, queue, and index changes operationally: cache variants/invalidation, worker routing/failure recovery, and bounded reindex behavior.
- Check distributable extension contents for secrets, debug statements, temporary files, duplicated translations, generated assets, and forbidden development artifacts.

## Accessibility

- Preserve semantic HTML and native controls. Flag clickable non-interactive elements, pseudo-buttons without keyboard behavior, positive `tabindex`, missing names/labels, invalid heading structure, and icons/images without appropriate text alternatives.
- Ensure navigation, filters, tabs, accordions, offcanvas panels, modals, quantity controls, cart, checkout, and account actions work by keyboard with visible, unobscured focus.
- Modals and offcanvas components must move focus to a useful entry point, contain focus appropriately, support expected close behavior, and return focus to the invoker.
- Associate form errors with fields using labels and `aria-describedby` or equivalent native semantics. Move focus or provide a clear summary when checkout submission fails.
- Announce asynchronous add-to-cart, coupon, shipping, login, and checkout results through an appropriate live-status mechanism without duplicating announcements.
- Verify repeated CMS, listing, card, modal, and form components produce unique IDs and valid ARIA relationships.
- Treat consent, keyboard, focus, status, zoom/reflow, and vendor accessibility for third-party widgets as first-class acceptance criteria.
- Map confirmed accessibility defects to relevant WCAG criteria and separate code evidence from browser/assistive-technology verification gaps.

## Internationalization and Commerce Context

- Use snippets for UI text and translation associations for entity content. Keep storefront and Administration snippet scopes explicit and keys namespaced.
- Verify snippet filenames and commands against the installed Shopware minor. For 6.7.3+ base-snippet conventions, keep locale-specific overrides intentional; preserve a compatible strategy for 6.6 when supported.
- Keep reads and writes language-aware and preserve inheritance/fallback behavior. Do not treat translated fields as generic custom fields.
- Use `SalesChannelContext` for storefront commerce decisions and derive DAL context from it only when needed. Generic `Context` is insufficient for pricing, tax, currency, shipping, rules, customer, and payment availability.
- Scope configuration and repositories by sales channel where values vary. Use the correct system-config inheritance instead of silently reading only global values.
- Recalculate authoritative commerce state after customer, address, currency, shipping, payment, or rule changes; presentation-layer visibility is not enforcement.

## Security and Performance Regression Scan

- Verify authentication, authorization, ownership, request authenticity, replay defense, rate limits, and method semantics at every state-changing entry point.
- Treat remote URLs, imports, callbacks, and downloads as SSRF-sensitive: allow safe schemes/hosts, reject private network targets where appropriate, set timeouts, cap redirects and payload size, and clean temporary files.
- Never expose secrets, Admin API credentials, private provider keys, signatures, context tokens, raw payment data, or sensitive customer data in logs, browser code, responses, exceptions, snapshots, or telemetry.
- Flag disabled TLS verification, untrusted request-host URL construction, unsafe deserialization, dynamic SQL without binding, and unsanitized rich HTML.
- Stress changes against large catalogs, customers, orders, languages, sales channels, imports, queues, and recurring batches. Identify the first unbounded query, loop, payload, cache key space, log table, or retry path.
- Check hot paths for external calls, repeated repository work, broad invalidation, synchronous side effects, heavy serialization, and unnecessary object graphs.
- Verify operational failure behavior: provider outage, queue outage/backlog, stale search index, failed migration/backfill, cache purge, partial webhook processing, and worker overlap must fail safely and remain recoverable.
