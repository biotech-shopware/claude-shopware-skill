# Quality and Operations

## Security Baseline

- Escape output by default and treat rich HTML as hostile unless it is sanitized.
- Prefer DAL to reduce injection risk. If raw SQL is necessary, bind every parameter.
- Treat any URL ingestion, remote file import, or webhook callback target as SSRF-sensitive: validate scheme and host, block private IP ranges, apply timeouts, and cap payload size.
- Use the official CSRF or request-authenticity protections for storefront or admin-initiated write flows where the platform expects them.
- Enforce ACL for admin operations and ownership checks for storefront or Store API operations.
- Never commit secrets. Treat system configuration values, API keys, and provider tokens as sensitive and keep them out of logs.
- Never set `verify => false` or equivalent TLS-disable flags in production HTTP clients.
- Distinguish browser-write routes from server-to-server endpoints. Browser-initiated POSTs need CSRF or equivalent request protection; webhooks and signed callbacks usually disable CSRF and replace it with sender authentication.
- State-changing customer-facing endpoints should be POST-only and protected against IDOR or ownership bypass. Do not expose mutations over GET.
- Do not log tokens, context tokens, provider responses, or payment payloads to the browser console or client-side telemetry by default.
- Do not treat `localStorage`, `sessionStorage`, or other browser-persisted values as authoritative payment, vault, or ownership state.

## External API Resilience

- Timeouts are mandatory.
- Use circuit-breaker or graceful-degradation behavior when a dependency can affect storefront, checkout, or admin usability.
- Favor queue-first synchronization and retries for non-interactive work.
- A provider outage must not crash the storefront, cart, checkout, or core admin workflows.
- Public callback or authorization endpoints need explicit hardening: signed tokens, bounded input, rate limiting, and narrow purpose.

Example patterns:

```php
// Bad: inline provider call in checkout path with no timeout or fallback
$quote = $this->shippingClient->fetchRates($cartPayload);
$cart->setExtension('shippingQuote', $quote);
```

```php
// Preferred: bounded timeout plus graceful fallback or cached quote
$quote = $this->shippingQuoteService->resolveQuote($cartContext);
if ($quote !== null) {
    $cart->setExtension('shippingQuote', $quote);
}
```

### Shipping and Tax Notes

- Do not block checkout on shipping-rate lookups; cache or decouple them where possible.
- Keep shipping method technical names and config migrations stable.
- Bound external tax calls in cart and checkout with caching, timeouts, and fallback behavior.
- Push reporting and other tax side effects into async processing.

## Observability

- Use structured logging with correlation IDs and actionable context.
- Log failures, retries, and state changes without dumping full request or response payloads.
- Redact tokens, signatures, secrets, and PII by default.
- Keep a lightweight audit trail for merchant support, but do not turn application tables into an unbounded log sink.
- If the domain stores order snapshots, cart snapshots, or provider payloads, keep only the minimum fields needed for support and reconciliation.
- Review recurring-payment and webhook logs specifically for leaked provider tokens, card identifiers, customer identifiers, signatures, and raw payload bodies.

## Cache, Queue, and Index Operations

- Treat cache variation, queue backlog, and indexer pressure as first-class rollout risks for Shopware 6.7 plugin changes.
- For cache-sensitive releases, verify anonymous/default, `cart-filled`, and `logged-in` state behavior explicitly because Shopware's HTTP cache and reverse proxies key off `sw-cache-hash` and invalidation states.
- Do not add cookies, cache-relevant headers, or session writes casually on storefront pages that should stay Varnish-safe.
- For production queues, prefer explicit transports for normal async work, low-priority work, and failed messages. Doctrine transport is acceptable for development; RabbitMQ or another dedicated transport is the expected production direction when load justifies it.
- A queue failure path is part of the design. Configure `failure_transport`, retries, and operator commands before rollout, not after the first stuck batch.
- Watch index rebuild cost after mapping or indexer changes: reindex duration, queue growth, DB load, and search fallback behavior.

Example patterns:

```yaml
# Preferred: explicit production-oriented transport split
framework:
  messenger:
    failure_transport: failed
    transports:
      async: '%env(MESSENGER_TRANSPORT_DSN)%'
      low_priority: '%env(MESSENGER_TRANSPORT_LOW_PRIORITY_DSN)%'
      failed: '%env(MESSENGER_TRANSPORT_FAILURE_DSN)%'
```

```text
Good cache rollout check:
- warm the changed page anonymously
- verify no new plugin cookie is set on the cacheable response
- verify cart-filled or logged-in state changes only the intended variant
- verify invalidation after a relevant entity update
```

## Testing and CI

- Unit-test core services.
- Integration-test DAL definitions, migrations, and critical flows.
- Use Store API or HTTP-level tests for custom routes and customer-facing API behavior.
- Use reusable fixtures or builders when repeated setup would otherwise hide intent.
- For frontend-heavy extensions, add smoke checks and compare Lighthouse results where performance risk is real.
- Improve PHPStan incrementally instead of freezing a huge baseline forever.
- Keep coding standards aligned with Shopware conventions.
- Do not ship or leave behind `die`, `exit`, or `var_dump`.
- Validate and package distributable extensions with Shopware CLI when the project uses it.
- For 6.7.3+ translation work, add `translation:lint-filenames` and `snippet:validate` to CI when possible.
- Run at least one container-compile or boot-path check when service wiring, decorators, handlers, or scheduled tasks changed.
- For cache, queue, or indexing work, add one targeted operational check: cache-hit behavior, worker consume path, failed-message command, or `dal:refresh:index` on a safe environment.

Concrete CI example:

```text
Good: after changing services.xml, a handler, and a scheduled task, run targeted tests plus one container boot or compile-path check instead of relying only on php -l.
```

## Store Readiness

- Test against the highest supported Shopware version before release.
- Keep the binary clean: do not ship unnecessary tests, CI config, editor settings, lock files, or other forbidden packaging artifacts.
- Register storefront cookies with the cookie consent manager when the feature sets them.
- For third-party storefront widgets or embeds, verify consent impact, keyboard/focus/status behavior, and ask for a VPAT or vendor accessibility statement when the feature is accessibility-sensitive. See `17-accessibility-and-template-best-practices.md` for the storefront audit baseline.
- Use store quality guidelines and store review errors as release gates, not as cleanup after the implementation is done.

## Common Failure Modes

Treat these as explicit regression checks:

- external HTTP calls in cart, checkout, or login without tight timeouts and fallback
- rendering user-specific HTML into cacheable responses
- DAL `search()` inside loops or other N+1 query shapes
- unbounded criteria queries or large blob hydration without batching
- broad cache invalidations on high-frequency events
- missing ACL or ownership checks
- logging secrets, tokens, or raw payloads
- browser console or client telemetry logging of tokens, context tokens, or payment payloads
- exposing Admin API credentials or private third-party keys to the storefront
- browser storage used as an authoritative source for saved-method, vault, or payment identity
- browser routes that disable CSRF without replacing it with the right security model
- GET endpoints that mutate customer data or order state
- internal plugins calling the shop's own HTTP API instead of shared services
- writes or recalculations triggered from storefront render events or read routes
- route duplication that drops core ACL or validation
- custom cookies or session writes added to cacheable storefront routes
- cacheable routes rendering customer-specific markup instead of isolating the fragment
- scheduled tasks with tiny intervals, unbounded scans, or duplicate handler registration
- scheduled tasks, reminders, or renewal workers that branch on translated state names instead of technical names
- invalid DAL association usage such as treating `customFields` like a normal association
- heavy blob hydration or full snapshot loading on large recurring batches without a clear need
- cache entries with unbounded growth because keys are serialized payloads and TTL is missing
- mutable operational flags stored in JSON payloads or custom fields and later queried at scale
- missing failure transport, retry strategy, or low-priority separation on production message queues
- indexer changes shipped without a bounded reindex plan or fallback check
- deep template copying instead of block extension
- copying core-only metadata into plugin code
- silent API contract changes without versioning or compatibility planning
- shipping dev artifacts or duplicated translation files in the plugin package

## Scheduled Tasks and Recurring Batches

- Batch due-item scans explicitly. Do not assume production data sets stay small.
- Keep loop control safe when external failures or partial processing happen. Do not advance business-critical schedule fields before success is known.
- Prefer technical names, stable IDs, or persisted state markers over translated labels in task logic.
- Avoid broad association trees in scheduled-task hydration unless every field is required for the batch decision.
- If a task stores snapshots or support data, put a bound on retention and growth.
