# Plugin Backend

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

## Migrations and Schema Safety

- Keep schema changes idempotent where possible.
- Keep large data backfills out of `update()`. Ship schema first, backfill asynchronously in batches, and add final constraints or indexes only after the data is ready.
- Separate destructive operations into `updateDestructive()`.
- Add indexes that match real filters, joins, and sort keys.
- Add composite unique indexes where they enforce idempotency or natural uniqueness for operational tables.
- Use parameter binding for manual SQL.

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
- Delay work with `DelayStamp` only when eventual consistency is acceptable and the retry story is clear.
- Keep handler side effects bounded. Re-read fresh state inside the handler instead of serializing whole entities into the message.

Example patterns:

```php
// Preferred: thin request path, async handoff with an explicit delay
$this->messageBus->dispatch(
    new SyncPartnerOrderMessage($orderId),
    [new DelayStamp(5000)]
);
```

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
