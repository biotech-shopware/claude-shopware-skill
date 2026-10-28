# Cache and HTTP Cache

Index: delayed invalidation, `CACHE_REWORK`, `sw-cache-hash`, cache state deprecations, ESI, Varnish/Fastly integration, removed classes, invalidation cost.

## Delayed Cache Invalidation

Shopware batches cache-tag invalidations by default in 6.7 (immediate in 6.6 unless configured).

The config key changed between majors — using the 6.6 name on 6.7 fails config validation with "Unrecognized option":

| Version | Key | Type | Default |
| --- | --- | --- | --- |
| 6.6 | `shopware.cache.invalidation.delay` | integer seconds | `0` (delayed invalidation **off**) |
| 6.7 | `shopware.cache.invalidation.delay_enabled` | boolean | `true` (delayed invalidation **on**) |

Delayed invalidation requires the `shopware.invalidate_cache` scheduled task to be running. Its cadence is a **separate** setting from the delay flag — see the interval section below; do not conflate them.

- Delayed storage: `shopware.cache.invalidation.delay_options.storage` — `mysql` by default; Redis for multi-node.
- If a plugin write must invalidate instantly (admin save that must show up in the storefront), send the `sw-force-cache-invalidate: 1` request header on the write.
- Debug pending invalidations: `bin/console cache:watch:delayed`.
- Flush pending invalidations manually: `bin/console cache:clear:delayed`.

Sources: Shopware 6.7 UPGRADE guide, release notes 6.7.0.

## CACHE_REWORK Feature Flag

`CACHE_REWORK` opts into the new Store-API HTTP-cache model. The older `CACHE_CONTEXT_HASH_RULES_OPTIMIZATION` flag still exists separately and is marked deprecated in favour of it — the two coexist, it was not a rename.

- **Opt-in and experimental.** `default: false` through 6.7.13 and still `default: false` on 6.8-dev. The *behaviour* is slated to become default in the next major, but do not assume the flag is on anywhere you have not checked.
- Makes **21** Store-API routes HTTP-cacheable via per-endpoint policies (12 pre-existing GET routes plus 9 added in 6.7.6).
- Cache stays active for logged-in customers and non-empty carts. Endpoints that must not cache per-user data must set `no-store` explicitly via the `_noStore` route attribute.
- Narrows `sw-cache-hash` to rule IDs flagged `RuleAreas::PRODUCT_AREA` — the product rule area, which is broader than and not the same as "price-relevant". Content varying by other rule areas must extend via `ResolveCacheRelevantRuleIdsExtension` or the `RuleAreas` DAL flag.

Source: release notes 6.7.5, 6.7.6.

## Finding Shape: Personalised Output In A Shared Response

Logged-in state is **not** customer identity. With `CACHE_REWORK`, cacheable Store-API responses stay cached for logged-in customers, so "the user is logged in" no longer implies "this response is private".

Any endpoint whose body varies by customer — prices, entitlements, saved addresses, wishlist state, tax exemption — and does not set `_noStore` is serving one customer's data to another from cache.

Report this as a **data-exposure defect**, not a merchandising or personalisation bug. The blast radius is every customer sharing that cache key, and the failure is silent: nothing errors, the wrong body is simply returned.

## What The HTTP Cache Key Varies On

`HttpCacheKeyGenerator` builds the key from the URL and query string, the `sw-cache-hash` cookie/header, and a fixed list of request headers (`HttpCacheVariantHeaders::HEADERS` in 6.7.15: `sw-access-key`, `sw-language-id`, `sw-currency-id`, `sw-include-seo-urls`). The `sw-cache-hash` value is built from rule IDs, version, currency, tax state, and logged-in state (`HttpCacheCookieEvent` parts).

Anything else does **not** split the cache, including `Accept-Language`, `X-Forwarded-For`/GeoIP, custom headers, and the guest's shipping country.

- If a cacheable page varies by something outside that list, add it to the hash in an `HttpCacheCookieEvent` listener (`$event->add('country', $countryId)`), or the first visitor's variant is served to everyone. Example: a free-shipping notice that depends on the visitor's country.
- With `CACHE_REWORK`/`PERFORMANCE_TWEAKS`, the rule-ID part narrows to the resolved rule areas (default `RuleAreas::PRODUCT_AREA`); see the `CACHE_REWORK` section.

### Redirects From Cacheable Routes Get Cached

`CacheResponseSubscriber` skips caching for 404s, non-GET requests, and routes without the `_httpCache` attribute. It does **not** skip 3xx responses. A redirect returned from a cacheable route (for example a language or country redirect on `frontend.home.page`) gets `s-maxage` and can be stored by the app cache, Varnish, or a CDN. Combined with the key above, one visitor's language decides where everyone is sent.

- Return redirects that depend on the visitor from a non-cacheable route, or mark the response private/`no-store`. On 6.7 without `CACHE_REWORK`, `setPrivate()` alone is not enough if `setSharedMaxAge()` runs later in the same response.
- Prefer `302` over `301` for visitor-dependent redirects. Browsers cache 301s indefinitely even when the shared cache doesn't.

## Deprecated Cache Symbols (removed in 6.8)

- `CacheStateValidator`
- `CacheStateSubscriber`
- `HttpCacheKeyGenerator::SYSTEM_STATE_COOKIE`, `CURRENCY_COOKIE`, `INVALIDATION_STATES_HEADER`
- Config: `shopware.cache.invalidation.http_cache`
- Env: `SHOPWARE_HTTP_DEFAULT_TTL` (and the whole group)

Do not reference these in new code. Warn when a plugin decorator uses them.

Source: release notes 6.7.6.

## Removed Store-API `Cached*Route` Classes

All `Cached<Foo>Route` Store-API decorators are deleted in 6.7.0. Caching now happens via HTTP cache policies (6.7.6+) or route attributes. Do not scaffold new `Cached*Route` classes; do not extend the removed ones.

Source: release notes 6.7.0.

## ESI Header And Footer

6.7.0 renders header and footer through Symfony ESI.

- New route names: `frontend.header`, `frontend.footer`. Paths: `/_esi/global/header` and `/_esi/global/footer` (the paths changed in 6.7.1; 6.7.0 used `/header` and `/footer`).
- New entry templates: `@Storefront/storefront/layout/header.html.twig` and `.../footer.html.twig`.
- New blocks in `base.html.twig`: `base_esi_header`, `base_esi_footer`.
- ESI render errors now throw; they were silently swallowed before.
- Requires ESI support in the reverse proxy (Symfony HttpCache, Nginx SSI/ESI, or Varnish). Configure `/_esi/global/header` and `/_esi/global/footer` in the proxy.

Extension pattern: extend `header.html.twig` / `footer.html.twig` directly. Pass extra data via `StorefrontRenderEvent` or the `headerParameters` merge, not inline `base.html.twig` block overrides (those blocks are now empty).

Source: release notes 6.7.0, UPGRADE-6.7.md §6.7.0.1.

## Varnish, Fastly, WebScale

External HTTP-cache plugins hook the Shopware cache-tag system.

- WebScale, Fastly, and similar plugins clear tags to their proxy — they do not clear Varnish directly.
- Never confuse `cluster_setup` (Symfony cache clustering across nodes) with HTTP cache. They are separate systems.
- The Symfony HttpCache app inside Shopware and an external reverse proxy in front of it can both cache. Tag invalidation must reach both.
- Nitro (Nuxt), Varnish/Fastly at the edge, and Shopware's own Symfony cache are three separate cache layers when a headless storefront sits in front. Invalidating one does not invalidate the others.

## Invalidation Cost Is Real

A single large surrogate-key purge (~45,000 keys observed on a single admin save) at an edge cache causes an origin TTFB spike ~8 seconds after the purge as misses arrive.

- Batch: keep delayed invalidation enabled in production (`delay_enabled: true` on 6.7, `delay > 0` on 6.6) so many small writes coalesce into one purge.
- Bound: never purge with unbounded tag arrays (e.g., "all products"). Prefer targeted tags.
- Observe: alert on edge-purge count and origin request-rate step-changes; correlate with admin activity.

## `NavigationRoute` Cache Key Event

`NavigationRoute` caches category level per sales channel in 6.7.

- Any plugin varying navigation by customer group, B2B context, or feature flag must subscribe to `\Shopware\Core\Content\Category\Event\CategoryLevelLoaderCacheKeyEvent` to add cache-key data. Note `Category\Event\`, not `Category\SalesChannel\` — a subscriber on the wrong FQCN registers cleanly and never fires.
- Without the subscription, navigation goes stale or leaks across contexts.

Source: UPGRADE-6.7.md §6.7.2.0, §6.7.3.0.

## Message Queue For Cache Work

Cache invalidation runs on a scheduled task (`InvalidateCacheTask`) that must actually execute.

- Production must run CLI workers with explicit transports and a failure queue. Do not rely on the admin worker.
- Interval default is 5 minutes on 6.7 (was 20 seconds on 6.6). If you customize it, run the scheduled task at the same or faster cadence.
- Enable `SHOPWARE_ES_THROW_EXCEPTION=1` in production so Elasticsearch outages fail loudly instead of silently falling back to MySQL and melting the primary.

Source: developer.shopware.com performance tweaks.
