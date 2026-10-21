# Storefront and Themes

Index: rendering, Twig, storefront JS, SCSS/theme, performance/cache, 6.7 structure, SEO/accessibility.

## Rendering Strategy

- Keep Twig templates cheap.
- Precompute data in controllers, page loaders, Store API routes, or dedicated services.
- Pass minimal context to templates.
- Extend templates with blocks before copying files.

## Twig Rules

- Use `sw_extends` and block overrides for upgrade safety.
- Do not copy full core templates unless block overrides or smaller partial overrides are insufficient.
- Keep autoescaping enabled.
- Avoid `|raw` on untrusted data.
- Do not hide business logic, authorization logic, or ownership checks in templates.
- Do not traverse heavy entity graphs or large collections in templates when the data can be prepared once upstream.
- Do not leave `dump()` or debug helpers in shipped templates.
- Use snippets for translatable text.
- Do not fetch database-backed data from Twig in loops or CMS slots via helpers such as `searchMedia()`. Resolve data once in a page loader, CMS resolver, or service.
- Do not use hard-coded static IDs in reusable product, listing, CMS, or account components.
- Do not use `href="#"` or similar pseudo-controls for button behavior.
- Do not use positive `tabindex`.
- Do not embed inline script or style blocks inside repeated product-card, slider, or CMS loops.
- Do not render customer-specific fragments or set plugin cookies from otherwise cacheable template paths just to personalize one label or banner.

Example patterns:

```twig
{# Bad: copied control markup plus pseudo-button navigation #}
<a href="#" class="buy-widget__toggle" onclick="toggleDetails()">
    {{ "my-plugin.details"|trans }}
</a>
```

```twig
{# Preferred: block-safe override with semantic control #}
{% sw_extends '@Storefront/storefront/component/product/card/action.html.twig' %}

{% block component_product_box_action_inner %}
    <button
        type="button"
        class="btn btn-secondary"
        aria-controls="product-details-{{ product.id }}"
        aria-expanded="false">
        {{ "my-plugin.details"|trans }}
    </button>
{% endblock %}
```

```twig
{# Bad: repeated IDs and expensive helper work in a listing loop #}
{% for product in searchResult %}
    <button id="details-toggle" aria-controls="details-panel">
        {{ "my-plugin.details"|trans }}
    </button>

    {% set media = searchMedia([product.coverId], context.context) %}
{% endfor %}
```

```twig
{# Preferred: instance-safe IDs and preloaded data prepared upstream #}
{% for product in searchResult %}
    <button
        type="button"
        id="details-toggle-{{ product.id }}"
        aria-controls="details-panel-{{ product.id }}"
        aria-expanded="false">
        {{ "my-plugin.details"|trans }}
    </button>
{% endfor %}
```

## Storefront JS

- Use the Shopware storefront plugin system and data attributes for progressive enhancement.
- Keep client code thin and avoid duplicating server-side business rules.
- Prefer Store API or purpose-built endpoints for dynamic data.
- Prefer native `fetch` for new storefront JS unless the project already standardizes on an existing HTTP helper.
- Do not embed secrets or privileged logic in storefront JS.
- Do not load third-party libraries globally when the feature only exists on one route or widget.
- Do not write untrusted HTML with `innerHTML`, `insertAdjacentHTML`, or equivalent sinks. Treat `v-html` with the same suspicion.
- Prefer `textContent` for status and label updates.
- Use `role="status"` or `role="alert"` for async UI feedback where users need an announcement.
- Manage focus explicitly for modals, flyouts, offcanvas panels, and other custom widgets that move the user through a stateful flow.
- Avoid browser `alert()` for recoverable failures or normal UI state changes.
- Scope selectors and event handling to the component root rather than broad document queries.
- Validate `postMessage` origins before trusting cross-window data.
- Escape data for JavaScript context explicitly; HTML escaping alone does not make inline JS safe.
- Do not inject the same external script, inline script, or inline style block inside product-card or CMS loops. Load once per page or route.
- Keep third-party widgets route-scoped and consent-aware.
- Throttle scroll handlers, constrain MutationObservers, and avoid polling loops that run across the whole storefront without a hard need.
- Do not use body-wide MutationObservers as the default way to repair labels, alt text, or other accessibility issues after render.
- Prefer Shopware's plugin registration and modal utilities over one-off global event wiring or bespoke modal shells.

```js
// Bad: global query and HTML sink in a repeated component
document.querySelector('.coupon-status').innerHTML = response.message;
```

```js
// Preferred: component-scoped update with safe text and status semantics
this.el.querySelector('[data-coupon-status]').textContent = response.message;
this.el.querySelector('[data-coupon-status]').setAttribute('role', 'status');
```

```js
// Preferred: consent-aware widget lifecycle
import Plugin from 'src/plugin-system/plugin.class';
import CookieStorage from 'src/helper/storage/cookie-storage.helper';
import { COOKIE_CONFIGURATION_UPDATE } from 'src/plugin/cookie/cookie-configuration.plugin';

export default class AnalyticsWidgetPlugin extends Plugin {
    init() {
        this.cookieStorage = new CookieStorage();
        this.toggleWidget();

        document.$emitter.subscribe(COOKIE_CONFIGURATION_UPDATE, () => {
            this.toggleWidget();
        });
    }

    toggleWidget() {
        this.el.hidden = !this.cookieStorage.getItem('my-plugin-analytics');
    }
}
```

```twig
{# Preferred: use Shopware's pseudo modal shell for route-scoped modal content #}
<button
    type="button"
    data-ajax-modal="true"
    data-url="{{ path('frontend.my-plugin.modal') }}">
    {{ "my-plugin.openModal"|trans }}
</button>
```

### Plugins Inside Replaced Markup Run Once

`PluginManager` initialises plugins on the DOM it finds. Some core widgets that refresh by replacing their markup don't re-initialise plugins inside the new content. `CartWidget` (`plugin/header/cart-widget.plugin.js`) sets `this.el.innerHTML` from session storage and again after each fetch. A plugin attached to an element inside the cart widget runs on the first render only, usually before the data it needs exists.

- Attach the plugin to an element **outside** the replaced markup and listen for the widget's events. `CartWidget` publishes `insertStoredContent` and `fetch` through its emitter, which dispatches them as DOM `CustomEvent`s on the widget element, so `addEventListener('fetch', …)` on `[data-cart-widget]` works.
- When your own code replaces markup that contains plugins, call `window.PluginManager.initializePluginsInParentElement(el)` afterwards.
- Carry data for JS in a `<template>` or `data-*` attribute rather than a hidden `<div>` inside a link. Templates are never rendered and screen readers skip them.

## SCSS and Theme Work

- Respect theme inheritance.
- Prefer variables, configuration, and stable CSS hooks over brittle selectors.
- Keep overrides local to the feature.
- Do not mix a large redesign with unrelated backend refactors.

### CSS Gotchas

- **Icons sit 0.25em low on purpose.** Core `_icon.scss` sets `.icon > svg { position: relative; top: 0.25em; }` to align icons with running text. In a flex row that already centres its items, the icon ends up a few pixels too low. Reset `top: 0` only for that component, not globally.
- **`overflow-x: hidden` on `html`/`body` breaks `position: sticky`.** `hidden` makes the element a scroll container, so sticky children stick to it instead of the viewport. To prevent horizontal scroll and keep sticky working, use `overflow-x: clip`.
- **Use `100dvh`, not `100vh`, for full-height mobile panels.** On iOS Safari `100vh` is the height with the toolbar collapsed. A menu sized `calc(100vh - …)` puts its bottom content behind the browser toolbar. `dvh` follows the visible viewport.
- **Find horizontal scroll at the source.** Common causes are fixed-width embeds (third-party iframes with a `width` attribute; give them `max-width: 100%`), the negative margins of a block's `.row` in a full-width CMS section, and fixed pixel font sizes that don't fit a 375px screen. Don't hide the overflow globally.
- **Bootstrap utilities sometimes use `!important`.** `.text-primary` and similar classes set their colour with `!important`. Overriding one in a single place needs a more specific selector *and* `!important`, scoped to that component. This is not the case anymore in newer versions of Bootstrap but will be true for any older existing projects or themes.

## Performance and Cache

- Treat storefront performance as a cache and payload problem first.
- Avoid adding cookies or headers on cacheable responses without a strong reason.
- Move user-specific fragments to AJAX, Store API, or non-cacheable routes rather than disabling cache broadly.
- Protect LCP by keeping hero media, server response time, and render-blocking CSS under control.
- Protect CLS by avoiding late banners, async style jumps, and unstable placeholders.
- Protect INP by keeping interaction handlers and storefront JS bundles small.
- If navigation, catalog visibility, or shipping/payment presentation varies by customer segment, rule, or sales role, enforce that variation server-side and ensure the cache key varies accordingly. Hiding it only in Twig is not a security boundary.
- Preserve cacheability of shared routes. If the page stays anonymous and cacheable, move customer-specific or high-churn fragments behind AJAX or purpose-built non-cacheable endpoints instead of forcing a whole-page miss.

## 6.7 Storefront Structure

- Review header and footer overrides carefully on 6.7 because shared fragment rendering changed.
- Re-check cache and template-target implications before copying older 6.6 storefront assumptions into 6.7 projects.
- Keep theme overrides block-scoped on 6.7 so shared fragment and cache-tag behavior stays aligned with upstream template changes.

## SEO and Accessibility

- Preserve canonical and SEO URL behavior when adding pages or custom entities.
- Keep landmarks, headings, labels, control relationships, and focus handling correct on checkout and interactive UI.
- Use buttons for actions and links for navigation.
- Prefer semantic HTML over ARIA patching. Only add advanced ARIA patterns when the full behavior is implemented.
- Use snippets and semantic HTML instead of hardcoded strings or div-heavy widgets.
- If the change adds tracking, embeds, or third-party storefront scripts, verify consent and store-readiness impact explicitly.
- Do not set global noindex or similar SEO-breaking directives from a theme override without scoping and intent.
- For deeper storefront accessibility requirements, U.S. ecommerce baseline guidance, and WCAG-oriented review output, also load `17-accessibility-and-template-best-practices.md`.

## 6.7 Storefront Changes

### `controllerName` / `controllerAction` → `activeRoute`

Deprecated in 6.7.3 across Twig, JS, and CSS.

- Twig: use `activeRoute` (already resolved) instead of `controllerName` + `controllerAction`.
- CSS: use `.is-active-route-*` classes instead of `.is-ctl-*` / `.is-act-*`. Generate the class with `activeRoute|replace({'.': '-'})`.
- JS: use `window.activeRoute` instead of `window.controllerName` / `window.actionName`.

Never emit the deprecated names in generated Twig, JS, or CSS.

Source: UPGRADE-6.7.md §6.7.3.0, release notes 6.7.3.

### Cookie Provider Replaced By Event

`CookieProviderInterface` is deprecated. Register cookies via listener on `\Shopware\Core\Content\Cookie\Event\CookieGroupCollectEvent` using `CookieEntry` / `CookieGroup` structs. The new Store-API route is `\Shopware\Core\Content\Cookie\SalesChannel\CookieRoute` → `/store-api/cookie-groups`.

Twig properties `snippet_name` / `snippet_description` are deprecated; use `name` / `description` (they handle both snippet keys and plain strings).

Source: UPGRADE-6.7.md §6.7.3.0.

### Global Storefront Event Bus (6.7.11+)

- `window.Shopware.emit('Namespace:Event', payload)` and `window.Shopware.on('Namespace:Event', handler)` provide a cross-plugin bus. Prefer this over ad-hoc `document.dispatchEvent`.
- `window.PluginManager.callPluginMethod(pluginName, methodName, ...args)` invokes a method on every live instance of a plugin. Prefer this over DOM lookups from another plugin.

Source: release notes 6.7.11.

### Vite Dev Server Replaces `composer watch:storefront`

`composer storefront:dev-server` provides HMR without a proxy on 6.7.11+. `composer watch:storefront` is deprecated. Fall back only when advising 6.6 / 6.7.0-6.7.10 projects.

Source: release notes 6.7.11.

### Theme Config As CSS Custom Properties

All `theme.json` fields (unless `scss: false`) are automatically exposed as native CSS variables using the SCSS name.

- Use `var(--sw-color-brand-primary)` for runtime theme swapping.
- Use SCSS variables only when the value must be resolved at compile time.

Source: release notes 6.7.11.

### `theme.json` Per-File References

`style` / `script` entries can point to `@BundleName/path/to/file.(scss|js)` for surgical overrides instead of pulling a whole bundle. 6.7.11+.

### `context.token` Removed From Twig

The Store-API context token is no longer exposed in Twig. Do not reference `context.token` in templates. If a plugin needs the token client-side, pass it explicitly via a controller-managed endpoint.

Source: release notes 6.7.5.0 — "The `context.token` variable is no longer available in twig rendering context to prevent potential security vulnerabilities."

Source: release notes 6.7.5.

### ESI Header And Footer

Header and footer render through ESI under route names `frontend.header` and `frontend.footer` (paths `/_esi/global/header` and `/_esi/global/footer` since 6.7.1; 6.7.0 used `/header` and `/footer`). New entry templates `@Storefront/storefront/layout/header.html.twig` and `.../footer.html.twig`. New blocks `base_esi_header` / `base_esi_footer` in `base.html.twig`.

- Extend `header.html.twig` / `footer.html.twig` directly. Do not override inline `base.html.twig` blocks that are now empty.
- Pass extra data via `StorefrontRenderEvent` or the `headerParameters` merge.
- ESI render errors now throw. Configure `/_esi/global/header` and `/_esi/global/footer` in the reverse proxy (Symfony HttpCache, Nginx SSI/ESI, or Varnish).

Full details in `23-cache-and-http-cache.md`.

Source: release notes 6.7.0.

### `sw_breadcrumb_full*` Requires `SalesChannelContext`

`sw_breadcrumb_full` and `sw_breadcrumb_full_by_id` require the full `SalesChannelContext` (not `context.context`). Call `sw_breadcrumb_full(category, context)` in Twig.

Source: UPGRADE-6.7.md §6.7.1.0.

### Accessibility Markup Baseline (EAA)

6.7.0 sets `$font-size-base: 1rem` (16px) and switches key controls to semantic markup:

- Language/currency widgets and pagination use `<button>` / `<a>` (not styled hidden radios).
- Cart line items are `<ul>` / `<li>` (not `<div>`).
- Product-card duplicate link removed — the image no longer wraps a second anchor.
- Modal triggers use `<button class="btn btn-link-inline">`.
- `{% sw_icon %}` sets `aria-hidden="true"` by default. When rendering an icon with meaning, pass `ariaHidden: false`.
- New modal snippet keys use `%…ModalTagOpen%` params. Prefer the `-Modal` snippet key variants.

Full accessibility guidance in `17-accessibility-and-template-best-practices.md`.

Source: release notes 6.7.0, UPGRADE-6.7.md §6.7.0.0.
