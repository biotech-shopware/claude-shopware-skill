# External API Caching In Cart

Index: why cart caching matters, mandatory cache contract, cache-key components, TTL rules, admin invalidation, live check on order placement, extendability, review prompts.

## Why This Is A Correctness Boundary

Shopware's cart calculation recalculates on many triggers. A single browser interaction (adding a line item, opening the cart) can trigger 2-6 cart calculations in the same PHP request. Any plugin that calls an external API — tax provider, shipping quoter, promotion service, personalization service — during cart calculation must cache the API response inside the request cycle and across requests.

The failure mode is not slowness. It is correctness: an uncached lookup returning different values across sequential calculations produces line-item prices, shipping totals, or tax that disagree with themselves within the same page load.

## Mandatory Cache Contract

Every plugin that calls an external API from a `CartDataCollectorInterface` or `CartProcessorInterface` implements this cache contract:

1. **Cache every response.** No pass-through calls during cart calculation.
2. **Use a deterministic cache key.** See the components list below.
3. **Set a TTL.** Never `null`, never "until manual purge only".
4. **Expose an admin invalidation route.** At least global; ideally per-customer.
5. **Support a live-check on order placement.** If the cache entry is older than a short "stale-if-order-imminent" threshold, refresh once before the order writes.

## Cache Key Components

A correct cache key is a hash of these values, in this order:

- Shipping origin (fixed plugin-config value: full address).
- Delivery address (country, ZIP, state/region, city, street) from the current `SalesChannelContext`.
- Cart amount (net or gross per provider requirement).
- Shipping amount.
- Line item fingerprint (product number + quantity + unit price per line, hashed).
- Provider-customer identifier (external customer id, tax-exempt group, etc.).
- Sales channel ID and currency ISO if the provider is currency-sensitive.

If any component changes, the key changes and the plugin re-fetches. Nothing else forces a refresh.

## TTL Rules

- Default TTL: **8 hours** for tax and shipping providers. Rationale: a customer shopping through the day is unaffected; a customer wrapping up at 5pm and returning at 8am expecting a status change (e.g., tax exemption) hits an expired entry and gets a fresh call.
- Shorter TTL (e.g., 15 minutes) for real-time-pricing providers.
- Never indefinite. Uncleared entries accumulate and cache storage fills over time.
- Auto-cleanup relies on TTL. Do not implement a custom LRU.

## Admin Invalidation Endpoint

Expose an Admin API route that invalidates the cache:

- `DELETE /api/_action/<plugin>/cache` — full cache invalidation for the plugin.
- `DELETE /api/_action/<plugin>/cache/{customerId}` — per-customer invalidation.

Guard both with `_acl` for a plugin-owned permission (e.g., `plugin.<name>.cache_clear`). Never expose from the storefront/Store API.

Add matching admin UI actions:

- One button on the customer detail page: "Clear cached <provider> data for this customer".
- One button in the plugin config: "Clear all cached <provider> data".

## Live Check On Order Placement

When the customer clicks "Place order":

1. Compute the cache key for the final cart.
2. If a cache entry exists and is older than the "live-check" threshold (e.g., 30 minutes), refresh once from the provider before writing the order.
3. If the refresh returns different tax/shipping/pricing, recalculate the cart and fail loudly to the customer rather than silently writing an order at the stale price.

This closes the "cart cached at 5pm, order placed at 8am, tax-exemption changed overnight" case.

## Extendability

Design the caching layer so a downstream plugin can decorate it.

- Put the external-API caller in a service tagged `<plugin>.provider`.
- Wrap it with a cache decorator tagged `<plugin>.provider.cache`.
- Expose the cache-key builder as its own service so a decorator can inject extra components (e.g., a promotion group).

A single-monolith caller inside a `Calculator` class blocks all downstream customization. If the plugin already ships that way, adding an admin invalidation endpoint and a TTL config option is the minimum acceptable change.

## Provider-Side Auto-Invalidation

The ideal case is: the provider notifies Shopware when a customer's status changes (e.g., TaxJar customer becomes tax-exempt), and Shopware invalidates the affected keys.

- This requires a webhook endpoint on the plugin's Admin API surface, signed and idempotent.
- Not all providers push status changes. When the provider does not, document the gap and rely on TTL + admin invalidation.

## Auditing An Existing Cache

The contract above is for a plugin with no cache. Auditing one that already has a cache is a different exercise, and checking the key against a fixed list is not enough — the list does not know what this provider returns.

Work from the payload, not from the list:

1. **Enumerate the fields of the cached payload.** What does the provider actually return, and which of those values does the plugin use?
2. **For each returned field, ask what inputs determine it.** A tax rate depends on delivery address, product tax class, and customer exemption status. A shipping quote depends on weight, dimensions, and origin.
3. **Name every value-determining input that is absent from the cache key.** Each one is a staleness bug: change that input, get the old answer.
4. **Check the inverse too** — inputs in the key that determine nothing. These fragment the cache and cost hit rate without buying correctness.

The output is a list shaped "field X depends on input Y; Y is not in the key," which is directly actionable and survives the provider adding fields later.

## Review Prompts

When reviewing a plugin that calls an external API in cart:

- Does every cart-time call go through a cache?
- What is the cache key? Does it include all seven components above?
- What is the TTL? Is there any indefinite entry?
- Is there an admin invalidation route? Is it ACL-protected?
- Is there a live-check on order placement?
- Can a downstream plugin extend the cache-key builder or replace the caller?
- Does provider-side status-change notification exist? If not, is that gap documented?

## Source

- Real-world TaxJar-plugin change request thread, `#webscale-shopware-altusnova` and `#sw-plugins`, August 2026.
- TaxJar plugin source: `github.com/solution25com/taxjar-shopware-6-solution25` (`Calculator.php` cache set with no expiration).
