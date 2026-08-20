# Cache and HTTP Cache

Index: delayed invalidation, `CACHE_REWORK`, `sw-cache-hash`, cache state deprecations, ESI, Varnish/Fastly integration, removed classes, invalidation cost.

## Delayed Cache Invalidation

Shopware batches cache-tag invalidations by default in 6.7 (immediate in 6.6 unless configured).

- Config key: `shopware.cache.invalidation.delay`. `0` = instant, `>0` = delayed and requires the `shopware.scheduled_task.invalidate_cache` scheduled task to be enabled.
- Default `delay` differs per version:
  - 6.6 default: `20` seconds.
  - 6.7 default with `cache_rework` active: `5 minutes` (300 seconds).
- Delayed storage: `shopware.cache.invalidation.delay_options.storage` — `mysql` by default; Redis for multi-node.
- If a plugin write must invalidate instantly (admin save that must show up in the storefront), send the `sw-force-cache-invalidate: 1` request header on the write.
- Debug pending invalidations: `bin/console cache:watch:delayed`.
- Flush pending invalidations manually: `bin/console cache:clear:delayed`.

Sources: Shopware 6.7 UPGRADE guide, release notes 6.7.0.

## CACHE_REWORK Feature Flag

`CACHE_REWORK` (renamed from `CACHE_CONTEXT_HASH_RULES_OPTIMIZATION` in 6.7.5) opts into the new Store-API HTTP-cache model.

- Default in 6.8. Optional in 6.7.
- Makes 12 Store-API endpoints HTTP-cacheable via per-endpoint policies: breadcrumb, category, navigation, CMS, product, seo-url, country, currency, language, salutation, media, cross-selling, reviews, search.
- Cache stays active for logged-in customers and non-empty carts. Endpoints that must not cache per-user data must set `no-store` explicitly via the `_noStore` route attribute.
- Narrows `sw-cache-hash`: only price-relevant rule IDs are included. Content that varies by other rules must extend via `ResolveCacheRelevantRuleIdsExtension` or use the `RuleAreas` DAL flag.

Source: release notes 6.7.5, 6.7.6.

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

- New routes: `\header`, `\footer`.
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

- Batch: leave `shopware.cache.invalidation.delay > 0` in production so many small writes coalesce into one purge.
- Bound: never purge with unbounded tag arrays (e.g., "all products"). Prefer targeted tags.
- Observe: alert on edge-purge count and origin request-rate step-changes; correlate with admin activity.

## `NavigationRoute` Cache Key Event

`NavigationRoute` caches category level per sales channel in 6.7.

- Any plugin varying navigation by customer group, B2B context, or feature flag must subscribe to `\Shopware\Core\Content\Category\SalesChannel\CategoryLevelLoaderCacheKeyEvent` to add cache-key data.
- Without the subscription, navigation goes stale or leaks across contexts.

Source: UPGRADE-6.7.md §6.7.2.0, §6.7.3.0.

## Message Queue For Cache Work

Cache invalidation runs on a scheduled task (`InvalidateCacheTask`) that must actually execute.

- Production must run CLI workers with explicit transports and a failure queue. Do not rely on the admin worker.
- Interval default is 5 minutes on 6.7 (was 20 seconds on 6.6). If you customize it, run the scheduled task at the same or faster cadence.
- Enable `SHOPWARE_ES_THROW_EXCEPTION=1` in production so Elasticsearch outages fail loudly instead of silently falling back to MySQL and melting the primary.

Source: developer.shopware.com performance tweaks.
