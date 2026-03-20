# Headless and Composable Frontends

## Core Contract Boundaries

Establish these boundaries before recommending fixes:

- which values are browser-authored hints versus server-authoritative facts
- where amount, currency, customer ownership, and payment success become authoritative
- which frontend values may be persisted locally and which must always be resolved server-side
- where provider truth is verified before local state is advanced

If the answers are unclear, keep tracing the flow before proposing a fix.

## Browser Trust Rules

- Do not persist authoritative vault IDs, saved-method identifiers, provider transaction IDs, or payment-success state in `localStorage`, `sessionStorage`, or similar browser storage.
- If the browser must keep a temporary reference, prefer an opaque server-issued value that cannot be used to widen account access on its own.
- Do not log access tokens, context tokens, provider responses, payment payloads, or vault identifiers to the browser console.
- Do not let request interceptors, debug hooks, or shared API clients widen credential exposure by logging headers, bodies, or tokens.
- Treat browser-authored payment, vault, or redirect data as untrusted until the backend re-resolves it in the correct customer and sales-channel scope.

Example patterns:

```js
// Bad: browser storage becomes saved-method authority
localStorage.setItem('selectedVaultId', providerVaultId);
```

```text
Preferred: persist only an opaque server-issued hint if truly needed, then resolve the current customer's saved method through an ownership-checked backend endpoint before payment or subscription mutation.
```

## Frontend Data Flow and Performance

- Defer PSP token fetches, vault-profile fetches, and similar provider calls until the customer selects the payment method or actively pays unless the UX truly requires earlier loading.
- Deduplicate cart, config, and payment-method fetches across components. Do not let each payment widget refetch the same backend data independently.
- Load third-party payment SDK scripts once per page or route. Do not let multiple components race to inject the same script.
- Keep fallback and error mapping centralized so one provider failure does not fragment the checkout UI into inconsistent states.

## Backend Contracts for Headless Payment Flows

- Public Store API or headless routes must never create authoritative local paid transaction rows from browser-authored input.
- Server-side code must derive payable amount, currency, customer ownership, and order context from the active cart, order, or trusted vault record before provider charge or payment-state mutation.
- Resolve the current customer's saved-method or vault record through a trusted backend lookup such as a `/me` style endpoint or another ownership-checked resolver. Do not trust raw browser-supplied vault IDs.
- Payment-link or hosted-checkout creation must use trusted configured callback targets. Do not accept success, failure, or return URLs from the browser as authoritative.
- Remove hard exits such as `echo`, `exit`, or `die` from request-path payment flows. Use normal exception and error-response handling.

## Review Prompts

Minimum questions to answer in a paired backend/frontend review:

- Can browser-authored data create or simulate a paid local transaction?
- Can a customer swap or replay a browser-stored vault or saved-method identifier to affect another customer?
- Does the frontend eagerly fetch provider data during checkout render that could be deferred until payment selection?
- Are payment SDK scripts, cart/config fetches, or provider-token requests duplicated across components?
- Are browser logs or telemetry leaking tokens, context identifiers, vault identifiers, or payment responses?
