# Payments

Index: non-negotiables, handler model, architecture, data collection, correctness, state sync, webhooks, saved methods, recurring/headless, validation.

## Non-Negotiables

- Never receive, store, or forward raw PAN, CVV, bank account, or routing data through your server.
- Treat client-reported payment state, amount, and provider identifiers as hints only.
- Mark a payment as successful only after server-side provider verification or a valid signed webhook.
- Keep checkout request-path work minimal.
- Make webhook processing signature-verified and idempotent.
- Keep admin operations behind Admin API plus ACL.
- Keep logs payload-minimal and secret-safe.

## Handler Model

For Shopware 6.7, start from the official payment guide:

- use `AbstractPaymentHandler`
- register with the `shopware.payment.method` tag
- expect `validate()` to be called
- expect `finalize()` when `pay()` returns a redirect response
- keep `validate()` fast and deterministic
- keep `finalize()` idempotent
- treat `supports(...)` checks for refunds or recurring flows as version-sensitive and confirm them against the exact core behavior
- create the payment method in `install()`, set `afterOrderEnabled` when needed, and deactivate on uninstall instead of deleting
- keep remote webhook/key provisioning out of generic `activate()` or `install()` side effects unless the setup is guaranteed idempotent and local-only; prefer explicit admin setup actions or commands for remote provisioning

For 6.6, open the archived guide first and verify the exact handler surface before reusing 6.7 assumptions.

## Recommended Architecture

Split responsibilities:

- payment handler
  Thin request-path entry point.
- payment orchestration service
  Intent/session creation, provider calls, retries, state normalization.
- transaction state sync service
  One place for Shopware transaction state transitions.
- webhook controller
  Raw body signature verification and fast acknowledgement.
- async processor
  Heavy webhook and reconciliation work.
- admin maintenance routes
  Webhook setup, diagnostics, manual repair actions.

## Data Collection

Use one of these patterns:

- provider-hosted redirect page
- provider-hosted fields
- provider JS tokenization

Persist only tokens or non-sensitive display metadata when the feature truly needs it.

Example:
- redirect flow
  `pay()` creates or updates the provider intent and returns a redirect, `finalize()` verifies the result, and a signed webhook or server-side verification remains the final authority.
- tokenized direct flow
  storefront JS sends only the provider token, while the backend attaches it to a server-created intent and verifies amount, currency, and merchant context server-side.

Code shape example:

```php
// Bad: browser token and request amount become local payment truth
public function pay(RequestDataBag $data, SalesChannelContext $context, AsyncPaymentTransactionStruct $transaction): RedirectResponse
{
    $this->transactionRepository->update([[
        'id' => $transaction->getOrderTransaction()->getId(),
        'stateId' => 'paid',
        'customFields' => ['provider_token' => $data->get('token')],
    ]], $context->getContext());

    return new RedirectResponse($data->get('successUrl'));
}
```

```php
// Preferred: persist operation intent, verify later, and keep local state server-authoritative
public function pay(RequestDataBag $data, SalesChannelContext $context, AsyncPaymentTransactionStruct $transaction): RedirectResponse
{
    $this->paymentOperationService->prepare(
        $transaction->getOrderTransaction()->getId(),
        $data->getAlnum('providerToken'),
        $context
    );

    return new RedirectResponse($this->paymentOrchestrator->createRedirect($transaction, $context));
}
```

## Correctness Rules

- Use `validate()` for prepared-payment invariants such as `orderTransactionId`, server-side prepared references, currency, amount, and merchant-account checks.
- Key provider operations by `orderTransactionId` or a provider-side unique reference.
- Persist an operation row before outbound provider calls and back it with unique indexes so retries return the previous result instead of duplicating side effects.
- Only verified payment handlers, verified callbacks, or reconciliation services may create authoritative local transaction rows or mark payment as successful.
- Make capture, refund, and webhook processing idempotent with persisted operation state and unique keys.
- Keep state transitions monotonic. Do not let a later duplicate event regress a final state.
- Correlate provider state to the correct Shopware transaction before changing anything.

## State Sync Service

- Route all transaction-state changes through one internal sync service.
- Apply Shopware transaction state handlers there, not ad hoc in controllers, handlers, or webhook code.
- Keep derived states such as partial refund vs full refund consistent.
- Treat disputes and chargebacks as distinct financial events, not as refunds.

## Webhooks

- accept only the expected method and content type
- verify signatures on the raw request body
- use constant-time comparison and the exact header/body canonicalization required by the provider
- check timestamp freshness or replay window
- allowlist event types
- persist provider event IDs with uniqueness so duplicate deliveries can acknowledge 2xx without reprocessing
- support secret rotation where the provider workflow needs active plus previous webhook secrets
- return quickly after enqueueing or persisting idempotency state
- do not perform slow provider reconciliation inline unless unavoidable
- keep provider verification helpers timeout-bound and audit-logged
- keep webhook management behind Admin API plus ACL; webhook endpoints are not admin endpoints
- build finalize or return URLs from trusted configuration or sales-channel domain data, not raw host headers from the incoming request

## Saved Methods and Refunds

- Enforce token ownership by customer and sales-channel context.
- Use provider tokens, not sensitive account data.
- Store local vault metadata explicitly: customer, sales channel, payment method, provider references, masked display metadata, status, and timestamps.
- Disable or soft-delete local records after provider-side detach where applicable.
- Align refunds with Shopware's order transaction model instead of inventing a parallel state machine.
- Trigger refunds from admin or automation flows, not storefront endpoints.
- Support partial refunds only with explicit idempotency and reconciliation rules.

## Recurring PSP Boundaries

- Load `15-subscriptions-and-recurring-payments.md` when subscription lifecycle, renewal scheduling, or multi-plugin recurring flow is in scope.
- Treat saved-card settings routes, recurring-preference AJAX routes, and subscription payment-method change routes as part of the payment trust boundary.
- Enforce ownership on saved cards, provider-choice records, and subscription-linked payment-method mappings by customer and sales-channel context.
- Keep provider recurring references scoped to the correct order transaction or local vault record and persist them only when the renewal flow truly needs them.
- Make finalize, recurring charge, and webhook flows agree on one authority for marking payment success.
- Keep recurring-operation identifiers idempotent across retries so duplicate task runs or duplicate callbacks cannot create duplicate provider side effects.
- If a subscription plugin persists a provider-specific choice, require the save step to be atomic with the payment-method change or clearly recoverable after failure.
- Review subscription-side helper endpoints with the same rigor as payment handlers, because they often decide which saved method will be charged later.

## Headless and Hosted Payment Contracts

- Load `16-headless-and-composable-frontends.md` when a separate frontend repo, composable checkout, or SDK package participates in the payment flow.
- Payment-link, hosted-checkout, or wallet-init routes must use trusted configured return URLs. Never accept success, failure, or callback targets from browser request bodies as authoritative.
- Do not charge the provider first from browser-authored headless payloads and then let Shopware discover the authoritative order state later. Re-establish server authority before money movement or local paid-state writes.
- Browser-authored transaction IDs, vault IDs, or provider references are hints only until the backend resolves customer ownership and provider state.

## Performance and Observability

- Do not block checkout on slow provider calls that can be verified later.
- Centralize provider HTTP clients with timeouts and safe retry policy.
- Reuse shared HTTP clients; do not instantiate clients per request.
- Add circuit-breaker behavior when provider slowness can exhaust workers or PHP-FPM capacity.
- Log correlation IDs, order transaction IDs, and provider references, not full payloads.
- If support needs recurring diagnostics, expose concise internal audit metadata instead of raw webhook bodies or full PSP responses.
- Store an internal audit trail when the payment domain needs long-lived supportability.
- If the support workflow needs it, expose a concise admin timeline or order detail panel based on audit data, not raw provider payloads.
- Track metrics when scale warrants it: invalid signatures, retries, refund failures, timeout rates, and queue backlog.

## Minimum Validation

- checkout pay/redirect/finalize path
- direct-pay path if present
- `validate()` success and failure for prepared payment invariants
- invalid or replayed webhook rejection
- duplicate webhook idempotency
- refund/capture retry safety
- saved-method ownership enforcement
- recurring charge or subscription payment-method change authority if present
- concurrency between admin refunds and webhook deliveries
- degraded-provider load behavior so timeouts and circuit breakers do not starve checkout workers

Cross-reference example:

```text
If the payment issue is really caused by collector or processor ordering, move the cart behavior into 18-cart-and-checkout-pipeline.md and keep only the payment authority rule here.
```

## 6.7 Payment Handler Contract

`AbstractPaymentHandler` consolidates five legacy interfaces:

- `SynchronousPaymentHandlerInterface`
- `AsynchronousPaymentHandlerInterface`
- `PreparedPaymentHandlerInterface`
- `RecurringPaymentHandlerInterface`
- `RefundPaymentHandlerInterface`

All are deprecated in 6.7. New payment plugins extend `\Shopware\Core\Checkout\Payment\Cart\PaymentHandler\AbstractPaymentHandler` and implement:

- `pay()`
- `finalize()`
- `validate()`
- `recurring()`
- `refund()`
- `supports()` — the capability check that gates recurring / refund / partial-refund flows

Register with a single DI tag: `shopware.payment.method`. Drop `.sync`, `.async`, `.prepared`, `.recurring`, `.refund` tags.

Handlers receive only `orderTransactionId`, request info, and `Context`. The handler must load its own order data — nothing else is passed.

Source: release notes 6.7.0; developer.shopware.com/docs/guides/plugins/plugins/checkout/payment/add-payment-plugin.html.

### `technicalName` Discipline

Payment method `technicalName` is non-nullable in 6.7 (auto-migrated). Always set a plugin-prefixed value:

```php
$paymentMethodData = [
    'handlerIdentifier' => MyPaymentHandler::class,
    'technicalName' => 'my_plugin_credit_card',  // required, plugin-prefixed
    // ...
];
```

If a plugin ships without `technicalName`, 6.7 assigns `temporary_<id>` — you lose stable reference for the method.

### SwagPayPal 6.7 Reference Architecture

Model complex payment plugins on the SwagPayPal 6.7 refactor:

- Single `AbstractPaymentMethodHandler` base class.
- One subclass per payment method (Credit Card, PayPal, Pay Later, etc.).
- Three lifecycle methods define the contract: `pay()`, `finalize()`, `executeOrder()`.
- Override `executeOrder()` for custom logic. Never duplicate core `pay`/`finalize`.
- Remove any references to deleted `AbstractPaymentBuilder` — replace legacy patch builders with standardized methods.

Source: shopware.com/en/news/optimizing-the-paypal-payment-handler-for-6-7-release/.

### Order `primaryOrderTransaction`

Since 6.7.1, `Order::primaryOrderTransaction` replaces `.transactions.first()`. The migration backfills existing orders. `OrderConverter` still puts the primary first in the collection for BC, but new code should read `order.primaryOrderTransaction`.

Same rule for `Order::primaryOrderDelivery`.

Source: release notes 6.7.1, UPGRADE-6.7.md §6.7.1.0.

## Cart Token vs Context Token

A common failure mode on shipping-quote and cart-preview routes.

- Overriding the cart token via a `sw-cart-token` GET parameter but not overriding the context token loads the correct cart items but **evaluates rules against the wrong context**. This surfaces as: only shipping methods available for the calling context are visible, but they are crosschecked against a different cart — producing wrong or missing shipping method options.
- The correct pattern: use the `sw-context-token` HTTP header to override the context. Both cart and context resolve consistently from the same token.
- Never accept cart-token override via query string for state-mutating routes. If a wishlist or shared-cart flow really requires it, document the constraint and gate the route with signed URLs plus expiration.

Source: real-world plugin review, August 2026.

## Middleware Retry = Duplicate Orders

When a headless or composable frontend reports "duplicate orders", the root cause is almost always a middleware retry loop, not a Shopware bug.

- Verify: what does the middleware do when the Shopware /store-api/checkout/order call returns a 5xx? A 4xx?
- Common wrong: retry on any non-2xx.
- Correct: retry only on network-level failure. On any HTTP response, inspect status and decide idempotently. Distinguish "order was actually created but response was lost" from "order was rejected".
- Shopware's `checkout/order` endpoint is not idempotent by client-provided key. If middleware needs safe retry, it must persist an idempotency key and check for an existing order before retrying.

Related: see `15-subscriptions-and-recurring-payments.md` and `16-headless-and-composable-frontends.md` for the multi-repo triangulation pass on this.

Source: real-world plugin review, `#altus-nova_shopware`, July 2026.

## External API In Cart (Tax, Shipping, Personalization)

Every payment or checkout plugin that calls an external API from cart processors must follow the caching contract in `24-external-api-caching-in-cart.md`:

- Cache every response with a TTL.
- Cache key includes shipping origin, delivery address, cart amount, shipping amount, line-item fingerprint, provider customer id, sales channel id, currency.
- Expose admin invalidation route (global + per-customer).
- Live-check on order placement if entry older than 30 minutes.

Source: real-world TaxJar plugin review threads, August 2026.
