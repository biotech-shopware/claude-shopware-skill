# Accessibility and Template Best Practices

Use sources in this order when accessibility is in scope:

1. Shopware official docs for the target version.
2. Stable Shopware core storefront behavior matching the locked version when docs are silent.
3. W3C WCAG 2.2 and WAI-ARIA APG patterns.
4. ADA.gov web guidance for U.S. business-accessibility framing.
5. U.S. Access Board ICT and Section 508 material as secondary reference.

## U.S. Ecommerce Accessibility Baseline

- Treat WCAG 2.2 AA as the default technical target.
- Keep WCAG 2.1 AA mapping in review output because it remains the most common U.S. litigation benchmark.
- Use ADA framing for business risk discussion, but keep findings technical and code-based.

Criteria that matter most in ecommerce storefronts:

- Non-text alternatives: product imagery, badges, icons, logos, payment icons, and decorative imagery must use meaningful alt text or empty alt where decorative.
- Color contrast and color-only cues: price drops, stock state, validation errors, and promotional badges cannot rely on color alone.
- Headings and landmarks: header, nav, main, search, footer, and account/checkout regions need a clear semantic structure.
- Keyboard access: navigation flyouts, filters, tabs, accordions, modals, offcanvas panels, quantity controls, and checkout widgets must be operable without a mouse.
- Focus order, focus visibility, and focus not obscured: custom modals, flyouts, sticky headers, and AJAX updates must preserve predictable focus behavior.
- Forms, labels, instructions, and error recovery: account, address, newsletter, stock alerts, checkout, coupon, and payment forms need explicit labels, instructions, and recoverable errors.
- Status messages and live regions: async add-to-cart, search suggest, stock alerts, coupon application, shipping-rate updates, and payment failures need announceable status changes.
- Zoom and reflow: header, PDP buy box, cart summary, checkout steps, and account tables must remain usable at 200% zoom and narrow widths.
- Target size minimum: small icon-only triggers in headers, wishlists, pagination, and product actions need enough hit area.
- Accessible authentication: login, checkout login, password reveal, and verification flows cannot rely on inaccessible puzzles or memory-only challenges.
- Captions and media handling where relevant: embedded media and product videos need captions or equivalent alternatives when audio carries information.

## Shopware 6.7 Storefront Alignment

- Prefer current 6.7 storefront markup, core templates, and extension points over older copied templates.
- Minimize full overrides of header, footer, navigation, search, account, cart, and checkout templates.
- If the project is on 6.6, explicitly check archived docs and do not assume 6.7 markup, JS hooks, or deprecation status.
- When Shopware docs do not spell out an accessibility behavior, fall back to stable core storefront behavior first, then W3C patterns.
- Do not use a copied legacy template as the accessibility baseline if newer core markup already fixed the issue upstream.

## Custom Theme and Twig Guidance

Start with semantic HTML:

- Use proper `header`, `nav`, `main`, `aside`, `footer`, `section`, list, table, and form semantics before adding ARIA.
- Use heading levels to reflect page structure, not styling needs.
- Use real lists for navigations, filters, breadcrumbs, and grouped actions.

Alt-text strategy:

- Prefer editorial alt and title values from media data.
- Use empty alt for decorative imagery.
- Never generate alt text from file names, URLs, or CSS class names.
- If an image is the only label for a link or button, ensure the control still has an accessible name.

Controls and relationships:

- Use buttons for actions and toggles.
- Use links for navigation and real destinations.
- Keep `aria-controls`, `aria-labelledby`, and `aria-describedby` valid and instance-specific.
- Do not ship repeated hard-coded IDs in product cards, listings, CMS slots, or repeated account widgets.
- Do not use positive `tabindex`.

Pattern discipline:

- Do not add `role="menu"`, `role="dialog"`, tabs, carousel roles, or combobox semantics unless the full APG interaction model is implemented.
- Prefer disclosure-style navigation or native Bootstrap/Shopware behavior over partial ARIA menu emulation.
- Avoid fake accessibility fixes through post-render DOM rewriting unless there is no safer extension surface.

Twig and render cost:

- Use `sw_extends` and block overrides before copying whole templates.
- Keep business logic, authorization logic, and ownership decisions out of Twig.
- Do not perform expensive Twig-side data loading or DB-backed lookup helpers in loops.
- Do not embed inline scripts or styles inside repeated product or CMS loops.
- Prepare data once in a page loader, subscriber, resolver, or service.

Example patterns:

```twig
{# Bad: repeated hard-coded ID and pseudo-control #}
<a href="#" id="filter-toggle" aria-controls="filter-panel">
    {{ "listing.filter"|trans }}
</a>
```

```twig
{# Preferred: instance-safe semantics #}
<button
    type="button"
    id="filter-toggle-{{ category.id }}"
    aria-controls="filter-panel-{{ category.id }}"
    aria-expanded="false">
    {{ "listing.filter"|trans }}
</button>
```

## Custom Storefront JS and Plugin Guidance

- Scope selectors and event handling to the component root, ideally `this.el`.
- Keep server authority on business rules, payment state, and ownership checks.
- Manage focus explicitly for modal, offcanvas, flyout, and payment UI.
- Return focus to the triggering control when the interaction closes.
- Use `role="status"` or `role="alert"` for async state changes such as alerts, coupon application, search suggest updates, shipping/payment failures, and order actions.
- Prefer `textContent` over `innerHTML` for status or label updates.
- Do not use browser `alert()` as the main UX for recoverable failures.
- Avoid broad `document.body` MutationObservers unless tightly bounded and temporary.
- Keep third-party widgets route-scoped and consent-aware.
- If an external widget cannot meet keyboard, focus, or status requirements, treat it as a first-class defect, not a best-effort enhancement.

Example patterns:

```twig
{# Preferred: modal trigger with instance-safe relationships #}
<button
    type="button"
    class="btn btn-primary"
    data-bs-toggle="modal"
    data-bs-target="#address-modal-{{ page.customer.id }}"
    aria-controls="address-modal-{{ page.customer.id }}">
    {{ "account.address.edit"|trans }}
</button>
```

```twig
{# Preferred: async status and error association for coupon or checkout feedback #}
<p id="coupon-status-{{ page.cart.token }}" class="visually-hidden" role="status" aria-live="polite"></p>
<input
    type="text"
    name="couponCode"
    aria-describedby="coupon-status-{{ page.cart.token }} coupon-error-{{ page.cart.token }}">
{% if error is defined %}
    <p id="coupon-error-{{ page.cart.token }}" class="text-danger">
        {{ error.message|trans }}
    </p>
{% endif %}
```

## Ecommerce Component Checklist

Review these surfaces explicitly when auditing a Shopware storefront:

- Navigation and flyouts: keyboard open/close, semantic structure, focus return, mobile/offcanvas parity.
- Search suggest and search results: label, live region, focus handling, result counts, empty state.
- Category filters and offcanvas filters: control labeling, checkbox/range semantics, apply/reset feedback, mobile focus.
- PDP media gallery, carousel, tabs, reviews, and buy widget: alt text, active state, keyboard control, quantity and variant selectors, add-to-cart feedback.
- Cart and checkout: focus order, error summary, shipping/payment async updates, coupon feedback, progress visibility, validation messaging.
- Account login, register, address, profile, and order history: form labels, required indicators, table responsiveness, modal behavior, async actions.
- Wishlist, newsletter, stock alerts, and price alerts: status messages, duplicate IDs, repeated-card interactions, email validation, opt-in messaging.
- CMS sliders, videos, embeds, and third-party widgets: controls, pause/stop where needed, captions, consent, and fallback content.

## Review Heuristics and Evidence Inputs

When `08-analysis-and-reviews.md` puts accessibility findings first, enrich each material accessibility finding with:

- path or surface
- affected flow
- WCAG mapping, with 2.1 AA relevance called out when useful
- failure mode
- blast radius
- smallest safe fix
- validation note

Differentiate clearly between:

- confirmed code-level accessibility defects
- runtime verification gaps that need browser or assistive-tech testing
- vendor or third-party widget limitations

If the user asks for a developer-ready review, include code examples or patch sketches for the safest fix direction.

## Anti-Patterns Learned From Reviews

Treat these as explicit red flags:

- `role="menu"` or similar ARIA patterns without the complete menu semantics and keyboard model
- filename-based alt generation
- duplicate IDs in reusable storefront components
- static `aria-controls` pointing at dynamic or missing targets
- anchor buttons using `href="#"`
- positive `tabindex` in modals or widgets
- `innerHTML` and `alert()` for async state changes
- body-wide MutationObservers used to repair accessibility after render
- `searchMedia()` or similar helpers inside Twig loops
- global `document.querySelector(...)` usage in storefront plugins that should be component-scoped
- modal close flows that do not return focus to the invoking control
- async add-to-cart, coupon, shipping, or checkout failures with no live status announcement
