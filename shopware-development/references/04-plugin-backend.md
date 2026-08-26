# Plugin Backend

Index: architecture, DAL/modeling, migrations, APIs, HTTP cache, performance, Messenger, external integrations.

## Architecture

Shape plugin backend code like a disciplined Symfony application:

- thin glue layer
  Controllers, subscribers, message handlers, scheduled tasks, Store API/Admin API routes.
- application services
  Business rules, orchestration, state transitions, idempotency, retries.
- infrastructure adapters
  DAL repositories, HTTP clients, SDK wrappers, filesystem access.

Keep orchestration out of controllers and subscribers.

## First Principles

- Treat every feature as either request-path code or background code. Request-path code must stay cheap.
- Protect hot paths first: cart, checkout, login, account, and any large admin listing.
- Treat cache hit rate, invalidation frequency, indexer backlog, queue backlog, and DB query count as the primary performance levers.
- Keep an uninstall and cleanup story for every custom entity row, custom field, config key, media asset, and scheduled operational artifact.

## Plugin Structure

Baseline structure:

- `composer.json` with PSR-4 autoloading
- `src/<Plugin>.php` kept thin
- `src/Service/`
- `src/Subscriber/`
- `src/MessageHandler/`
- `src/Migration/`
- `src/Resources/config/services.xml`

Use install/update lifecycle code only for plugin lifecycle concerns, not general business behavior.

## Compatibility and Upgrade Safety

- Pin supported Shopware packages conservatively. Avoid broad wildcard constraints.
- Prefer documented extension points and stable core patterns over `@internal` behavior.
- Do not copy core-only metadata such as `#[Package(...)]` or `@internal` tags into plugin public code.
- If a design intentionally couples to a fragile event payload or core behavior, document that coupling explicitly.

## DI and Service Design

- Use constructor injection only.
- Avoid `$container->get()` in runtime code.
- Prefer decoration or events over replacing core behavior by inheritance.
- Wrap external clients in services that centralize timeouts, retries, and logging policy.
- Prefer one reusable seam over duplicated near-identical services when the behavior is actually shared.

## DAL and Data Modeling

- Use DAL first; fall back to DBAL only when necessary.
- Load only required associations. Do not hydrate full entity graphs by default.
- Prefer `searchIds()` when only identifiers are needed, then fetch a second time only if full entities are required.
- Never call repository `search()` inside loops over entities or line items. Treat that as a classic N+1 failure.
- Paginate admin lists, exports, and sync jobs rather than assuming bounded result sizes.
- Treat unbounded criteria queries as production incidents waiting to happen on large shops.
- Avoid pulling large serialized blobs such as cart payloads unless absolutely necessary; batch and cap memory if you must.
- Use custom fields for merchant-managed metadata, not write-heavy operational data.
- Use entity extensions or custom entities for structured domain state.
- Do not use mutable JSON payload fields on line items, orders, or logs as primary operational query state. If you need to query or deduplicate by that state, model it in indexed columns or a custom entity instead.
- Merge existing custom fields instead of overwriting the full array unless replacing everything is intentional and safe.
- Do not add redundant casting, trimming, or null fallback logic after a typed DAL read or validated config read unless there is a concrete failure mode in that path.

Entity extension decision matrix:

| Need | Prefer | Avoid when |
| --- | --- | --- |
| a few merchant-managed values on an existing entity | custom fields | the data drives high-volume writes, deduplication, or indexed operational queries |
| structured fields attached to an existing entity with code ownership | entity extension | the state really has its own lifecycle or needs standalone queries |
| standalone operational state, dedupe keys, sync history, or batch processing | custom entity | the data is just editorial decoration on an existing entity |
| merchant-defined structure in 6.7+ where dynamic entities truly fit the requirement | dynamic custom entities | the requirement needs plugin-owned behavior, strict invariants, or broad 6.6 support |

Example patterns:

```php
// Bad: full entity hydration just to collect IDs inside a loop
foreach ($customers as $customer) {
    $criteria = new Criteria();
    $criteria->addFilter(new EqualsFilter('customerId', $customer->getId()));

    $orders = $this->orderRepository->search($criteria, $context);
    $this->syncOrderIds($orders->getIds());
}
```

```php
// Preferred: batch IDs first, then fetch only what is needed
$criteria = new Criteria();
$criteria->addFilter(new EqualsAnyFilter('customerId', $customerIds));

$orderIds = $this->orderRepository->searchIds($criteria, $context)->getIds();
$this->syncOrderIds($orderIds);
```

```php
// Bad: loading full associations and blobs for an admin list
$criteria = new Criteria();
$criteria->addAssociation('lineItems');
$criteria->addAssociation('transactions');
$criteria->addAssociation('addresses');
```

```php
// Preferred: bounded list query plus targeted fields
$criteria = new Criteria();
$criteria->setLimit(50);
$criteria->setOffset($offset);
$criteria->addAssociation('transactions.stateMachineState');
$criteria->addFields(['id', 'orderNumber', 'createdAt']);
```

```php
// Preferred: merge custom fields instead of replacing unrelated state
$payload = [
    'id' => $orderId,
    'customFields' => [
        ...($order->getCustomFields() ?? []),
        'my_plugin_sync_state' => 'queued',
    ],
];
```

```php
// Bad: redundant normalization after a validated non-null string read
$code = trim((string) $config->getWebhookCode()) ?? '';
```

```php
// Preferred: use the typed value directly when the contract already guarantees it
$code = $config->getWebhookCode();
```

## Migrations and Schema Safety

- Keep schema changes idempotent where possible.
- Keep large data backfills out of `update()`. Ship schema first, backfill asynchronously in batches, and add final constraints or indexes only after the data is ready.
- Put every change the plugin needs into `update()`. Plugin install and update **never** call `updateDestructive()` — it is reachable only from `bin/console database:migrate-destructive`, which merchants effectively never run for plugins. Work placed there silently never executes. Handle removal in `uninstall()`. See `26-plugin-lifecycle-and-activation.md`.
- Add indexes that match real filters, joins, and sort keys.
- Add composite unique indexes where they enforce idempotency or natural uniqueness for operational tables.
- Use parameter binding for manual SQL.
- Do not edit already executed migration classes; add a new migration unless the repo explicitly has a safe local-only migration policy.

## Store API and Admin API

- Keep routes thin and decoratable.
- Apply the correct route scope and permissions.
- Expose storefront-relevant behavior through Store API when headless use is plausible.
- Prefer cacheable reads where it is safe and make writes clearly non-cacheable.
- Enforce ownership server-side on Store API routes. Never expose privileged operations there.
- Keep privileged operations behind Admin API plus ACL.
- Keep API error shapes consistent and avoid leaking internal exception details through public responses.
- Version or isolate externally consumed contracts when breaking changes would affect headless or third-party clients.
- Apply rate limiting deliberately on abuse-prone or public endpoints, not blindly across trusted internal flows.
- Never accept raw `Criteria`, arbitrary associations, or client-selected query complexity directly from request payloads. Whitelist filters, pagination, sorting, and include depth explicitly.
- Keep headless endpoints bounded. Do not return "all snippets", "all entities", or deep graphs without a pagination and payload-size strategy.
- Public Store API or headless payment routes must never create authoritative local paid transaction rows or decide payment success from browser-authored inputs.
- For headless payment flows, derive amount, currency, and order context from server-side cart or order recalculation before any provider charge or local payment-state write.
- Resolve current-customer vaulted or saved-payment records server-side. Do not accept raw browser-stored vault identifiers as authoritative without ownership resolution.
- Prefer decorating services or inner routes over redefining existing public routes. Route duplication or controller copy-paste often drops ACL, validation, or behavior guarantees.
- Do not call your own shop's Admin API or Store API over HTTP from backend code in the same project. Inject the underlying services or repositories directly.
- If multiple valid persistence flows exist, pause before choosing when the decision changes entity save behavior, immediate-write behavior, or the data model.
- If plugin-owned data conceptually belongs to the parent entity edit flow, prefer the normal entity save pipeline by default.

Keep detailed collector, processor, validator, delivery, and promotion pipeline rules in `18-cart-and-checkout-pipeline.md` instead of expanding this file with cart internals.

## HTTP Cache and Reverse Proxy Safety

- Mark storefront routes cacheable only when they are `GET`-only, read-only, and state-safe.
- For custom storefront controllers, use `defaults: ['_httpCache' => true]` and load data through page loaders or Store API routes so core cache tags remain authoritative.
- `sw-cache-hash` already captures cache-relevant state such as login, cart, currency, tax, and matched rules. Do not create extra variation with custom cookies or ad hoc headers unless the response truly differs.
- `sw-invalidation-states` can intentionally skip cache for states such as `logged-in` and `cart-filled`. Prefer Shopware's state model over plugin-specific cache-busting.
- Never touch the session, set custom cookies, or render customer-specific markup from an otherwise cacheable route just to personalize a small fragment. Split that fragment into AJAX, ESI, or a dedicated non-cacheable endpoint.
- Cacheable controller routes inherit invalidation from the Store API tags used to build the page. Avoid parallel invalidation logic unless the route truly loads plugin-owned data outside the normal Store API surfaces.

Example patterns:

```php
// Bad: cacheable route mutates session state and renders personalized data
#[Route(path: '/promo', name: 'frontend.my-plugin.promo', methods: ['GET'], defaults: ['_httpCache' => true])]
public function promo(Request $request, SalesChannelContext $context): Response
{
    $request->getSession()->set('my_plugin_seen', true);

    return $this->renderStorefront('@MyPlugin/storefront/page/promo.html.twig', [
        'customerName' => $context->getCustomer()?->getFirstName(),
    ]);
}
```

```php
// Preferred: keep the page cacheable and move personalization behind a separate endpoint
#[Route(path: '/promo', name: 'frontend.my-plugin.promo', methods: ['GET'], defaults: ['_httpCache' => true])]
public function promo(): Response
{
    return $this->renderStorefront('@MyPlugin/storefront/page/promo.html.twig');
}

#[Route(path: '/widgets/promo/customer-badge', name: 'frontend.my-plugin.promo.customer-badge', methods: ['GET'])]
public function customerBadge(SalesChannelContext $context): JsonResponse
{
    return new JsonResponse([
        'firstName' => $context->getCustomer()?->getFirstName(),
    ]);
}
```

## Performance, Cache, and Async

- Treat cart, checkout, login, account, and high-volume queries as hot paths.
- Do not block request paths on external I/O unless absolutely required.
- Push expensive derived data or sync work into Messenger, indexers, or scheduled tasks.
- Separate low-priority or bulk background work from checkout-sensitive consumers when queue backlog could affect customer-facing flows.
- Plan for reverse proxy, CDN, and Varnish-style caching behavior.
- Avoid cache-key explosions from extra cookies, headers, or highly dynamic fragments.
- Do not assume "logged-in users disable HTTP cache" as a permanent invariant.
- If user-specific data is required, make it explicit with AJAX, ESI fragments, or non-cacheable routes rather than globally disabling cache.
- Before increasing cache variation or invalidation frequency, estimate the hit-rate impact and state the least destructive alternative.
- Do not perform DAL writes, entity updates, or expensive recalculations inside storefront read routes or generic render events just to decorate response data. Use runtime extensions, response extensions, or cacheable precomputation.
- Avoid `order.written` or state-transition subscribers that write the same entity again or call external systems synchronously. That pattern creates recursion, duplicate processing, and checkout latency.
- Normalize cache keys and set TTLs for external-quote or derived-data caches. Never cache entire serialized request payloads forever.

## Messenger and Handler Patterns

- Use explicit message classes plus idempotent handlers for async work. Persist dedupe or state-transition guards before dispatch when duplicates would hurt.
- Prefer separate transports for checkout-sensitive async work and low-priority bulk work.
- On Shopware, move non-urgent work to `low_priority` via `LowPriorityMessageInterface` or `shopware.messenger.routing_overwrite` instead of letting it compete with checkout-adjacent async work.
- Do not use Symfony `DelayStamp` as a portable Shopware default because it is not compatible with every supported Messenger transport. Prefer a scheduled task or persisted due-time queue when delayed execution is required; use transport-specific delay only after the project proves support.
- Keep handler side effects bounded. Re-read fresh state inside the handler instead of serializing whole entities into the message.

Example patterns:

```php
// Preferred: mark clearly non-urgent work as low priority
final class RebuildPartnerSnapshotMessage implements LowPriorityMessageInterface
{
    public function __construct(private readonly string $customerId)
    {
    }
}
```

```php
// Preferred: transport-specific, idempotent handler
#[AsMessageHandler(fromTransport: 'low_priority')]
final class SyncPartnerOrderHandler
{
    public function __construct(
        private readonly SyncLogService $syncLogService,
        private readonly PartnerSyncService $partnerSyncService
    ) {
    }

    public function __invoke(SyncPartnerOrderMessage $message): void
    {
        if ($this->syncLogService->alreadyProcessed($message->getOrderId())) {
            return;
        }

        $this->partnerSyncService->syncOrder($message->getOrderId());
    }
}
```

```php
// Bad: serializing mutable entities or large payloads into the message
$this->messageBus->dispatch(new SyncPartnerOrderMessage($orderEntity, $request->request->all()));
```

## External Integrations

- Centralize HTTP clients.
- Set explicit timeouts.
- Prefer retries only for safe, idempotent operations.
- Add circuit-breaker or fallback logic when the dependency can degrade the shop.
- Queue non-interactive sync work.
- Never disable TLS verification in production clients.
- Do not build callback or return URLs from `HTTP_HOST` or other untrusted request host headers. Use configured sales-channel domains or explicit trusted configuration.

If the integration is a payment provider, stop here and load `07-payments.md`.

## 6.7 Core Changes That Affect Backend Code

### Migrations And Schema

- **FK naming changed** in the migration generator / `SchemaBuilder` from `fk.<table>.<column>` to `fk__<table>__<column>` (double underscore). This applies to **newly generated** constraints; constraints already present in a migrated database keep their old names. Audit both spellings when a migration drops or renames a foreign key by string. Source: release notes 6.7.8.
- **Translation-table references** now use `ON DELETE CASCADE` in new migrations.
- **Use `\Shopware\Core\Framework\Util\Database\TableHelper`** for schema introspection. `EntityDefinitionQueryHelper::columnExists()` and `tableExists()` are deprecated in favour of it. `columnIsNullable()` is deprecated as unused and has **no** `TableHelper` replacement.
- **`MigrationStep` named-parameter renames** — the table parameter is still `$table`, do not rename it:
  - `dropColumnIfExists`: `column` → `columnName`
  - `dropForeignKeyIfExists`: `column` → `foreignKeyName`
  - `dropIndexIfExists`: `index` → `indexName`

### `EntityDefinition::__construct` Deprecated

Calling `parent::__construct()` from an `EntityDefinition` subclass is deprecated for the next major. Do not emit `parent::__construct()` in generated entity definitions.

Source: UPGRADE-6.7.md §6.7.2.0.

### Custom Field Naming

Custom field names may no longer contain hyphens or dots — they are used directly as Twig variable names. Use `snake_case`.

### `ScheduledTaskHandler` Requires `LoggerInterface`

Since **6.7.0.0**, `ScheduledTaskHandler` requires a non-nullable `Psr\Log\LoggerInterface` constructor argument (it was optional and nullable in 6.6). Handlers registered through the container — the standard plugin path — need no change; hand-constructed handlers hit `ArgumentCountError`.

Separately, from **6.7.13** the protected `markTaskRunning()`, `markTaskFailed()`, and `rescheduleTask()` hooks are deprecated. Rely on the framework for run/failure/reschedule bookkeeping.

Source: release notes 6.7.13; `ScheduledTaskHandler` constructor at v6.6.10.6 vs v6.7.0.0.

### Messenger Message Size Limit

Message-size enforcement is **opt-in and off by default**:

- `shopware.messenger.enforce_message_size` — `defaultFalse()`. The size listener returns early while this is false, so nothing is capped out of the box.
- `shopware.messenger.message_max_kib_size` — default `1024` KiB; applies only when enforcement is enabled. `0` disables.
- Design messages to reference DB rows instead of carrying blobs regardless of the setting. Do not raise the limit as a first response — small messages are the correct long-term pattern.

Source: `Framework/DependencyInjection/Configuration.php` (`enforce_message_size` `defaultFalse()`, `message_max_kib_size` `defaultValue(1024)`); `MessageQueueSizeRestrictListener`.

### Webhook Messenger Transport (`WEBHOOKS_REWORK`)

Default in 6.8. With `WEBHOOKS_REWORK` on, webhooks get a dedicated DB-backed Messenger transport with fair scheduling and a retry ladder: 5s → 30s → 5min → 30min → 4h.

- Consumers must include `webhook` in the transport list:
  ```bash
  bin/console messenger:consume webhook async low_priority
  ```
- `shopware.admin_worker.transports` must be prepended with `webhook`.
- Rollback path: `bin/console webhook:drain-to-async`.

Source: release notes 6.7.12, UPGRADE-6.7.md §6.7.12.0.

### `NavigationRoute` Cache Key Event

Default category levels are now cached per sales channel. Dynamic navigation must subscribe to `\Shopware\Core\Content\Category\Event\CategoryLevelLoaderCacheKeyEvent` to add cache-key data. Without the subscription, navigation goes stale or leaks across contexts.

Note the namespace: `Category\Event\`, not `Category\SalesChannel\`. A subscriber keyed on a wrong FQCN still registers cleanly — `::class` resolves at compile time without an existence check — and then never fires, producing exactly the stale/leaked navigation this rule exists to prevent.

Source: UPGRADE-6.7.md §6.7.2.0, §6.7.3.0.

### Sync API Foreign-Key Resolvers

From 6.7.11 the Sync API accepts human-readable keys instead of UUIDs:

- `currency.iso_code`
- `locale.code`
- `payment_method.technical_name`
- `shipping_method.technical_name`
- `document_type.technical_name`
- `salutation.salutation_key`
- `tax.tax_rate`

Prefer these over UUID lookups in import/sync code.

Source: release notes 6.7.11.

### State Machine Per-Entity Locking

From 6.7.11 `StateMachineRegistry::transition()` acquires per-entity locks to prevent duplicate history entries on concurrent transitions. Do not implement custom mutex/dedup logic around state transitions.

Source: release notes 6.7.11.

### Store-API `limit` Cap

`shopware.api.store.max_limit` (default 100) caps the `limit` parameter on `/store-api/product-listing/{categoryId}`, `/store-api/search`, and `/store-api/search-suggest`. Fetch in pages; do not request unbounded limits.

From 6.7.13 Store-API requests no longer start PHP sessions unless code explicitly does. Do not rely on side effects that depended on session start (e.g., cart token in `$_SESSION`).

Source: UPGRADE-6.7.md §6.7.3.0, release notes 6.7.13.

### `ResetInterface` For Long-Running Runtimes

For FrankenPHP / RoadRunner runtime compat, any custom service holding request-scoped state (per-request caches, current context) must implement `Symfony\Contracts\Service\ResetInterface::reset()` to clear it between requests.

Source: release notes 6.7.2.

### Product `states` → `type` Model

`product.states`, `order_line_item.states`, `LineItem::$states`, `StatesUpdater`, `ProductStatesBeforeChangeEvent`, and `ProductStatesChangedEvent` are deprecated in 6.7.7 in favor of `product.type` and `order_line_item.payload.product_type` / `LineItem::$payload['productType']`. Register custom types via `shopware.product.allowed_types` config.

Source: release notes 6.7.7.

### Sales Channel Repository Default

Prefer sales-channel repositories to fetch data even when the project has only one sales channel. When many rules or plugins depend on that pattern, retrofitting later is expensive.

If a plugin truly runs against exactly one sales channel with no filtering, document the deliberate skip.

### Hard Limits On Data Fetches

Always add a hard limit to plugin queries, even when a natural bound seems to exist. A schema change or data-model surprise can turn a "small" query into a runaway. Prefer `setLimit()` and pagination over any unbounded assumption.

## Cross-References

- Cache and HTTP cache details: `23-cache-and-http-cache.md`.
- Cart, checkout, delivery, promotion pipeline: `18-cart-and-checkout-pipeline.md`.
- External API caching in cart (tax, shipping providers): `24-external-api-caching-in-cart.md`.
- Testing patterns: `19-testing-patterns.md`.
- Patching, PHPStan, Frosh Tools: `25-patching-and-dependency-tooling.md`.

