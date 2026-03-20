# Storefront and Themes

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

## SCSS and Theme Work

- Respect theme inheritance.
- Prefer variables, configuration, and stable CSS hooks over brittle selectors.
- Keep overrides local to the feature.
- Do not mix a large redesign with unrelated backend refactors.

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
