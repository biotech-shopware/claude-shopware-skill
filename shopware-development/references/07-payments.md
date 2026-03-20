# Payments

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
