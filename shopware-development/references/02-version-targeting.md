# Version Targeting

## Default Rule

Default to Shopware 6.7 guidance. Switch to explicit 6.6 compatibility mode when:

- the root project or plugin constraints cap Shopware at `6.6.*`
- the user says the work must remain 6.6-compatible
- the repo contains transition-era admin or payment code that should not be silently migrated

## Detection Order

Check in this order:

1. Root `composer.json`
2. Plugin/theme/app `composer.json`
3. `composer.lock`
4. Existing code patterns that imply a versioned extension surface

State the version assumption before changing behavior.

## 6.7-First Deltas

Use these as default assumptions for 6.7 work:

- Payments
  Official 6.7 docs show the single `AbstractPaymentHandler` flow, `validate()` always being called, and `finalize()` being called when `pay()` returns a redirect response.
- Administration
  Use the official Vue 3, Pinia, and Vite migration docs when the task includes admin modernization. Treat these as explicit migrations, not incidental cleanup.
- Translations
  Shopware 6.7.3 introduced the country-independent snippet base layer. Use base files such as `messages.en.base.json` and `messages.de.base.json`, keep country-specific files as small overrides, preserve empty former country-specific files where backward compatibility needs them, and validate with `translation:lint-filenames` plus `snippet:validate`.
- Caching
  Follow the current cache and HTTP cache docs. Do not depend on legacy assumptions like "logged-in users always disable cache."

## 6.6 Compatibility Rules

When the project targets 6.6:

- Open the archived docs under `/docs/v6.6/` before relying on a 6.7-only pattern.
- Keep admin migrations explicit. Do not force Pinia or Vite unless the project is already migrating.
- Treat 6.7 translation-layer improvements as optional, not assumed.
- Re-check payment handler contracts and extension points against 6.6 docs before applying 6.7 examples.

## Compatibility Strategy

Use the least risky path:

- If behavior can stay version-neutral, do that.
- If the implementation must differ, isolate the version-sensitive seam in one service or adapter.
- If the task would require a wide migration, stop and name it as a separate chunk rather than mixing it into a feature change.

## Migration Playbook

When the task is an upgrade, scan first and migrate second.

Check these surfaces explicitly:

- payment handlers, prepared-payment validation, and redirect/finalize flow
- admin build stack and state management assumptions
- copied Twig templates or old storefront JS hooks
- snippet filename conventions and fallback behavior
- service decoration against fragile or deprecated core services
- tests that depend on older bootstrap or admin assumptions

Concrete scan examples:

Example patterns:

```text
Bad: "While touching this admin module, also migrate it from Vuex to Pinia."
Good: Keep the feature fix version-neutral unless the task is explicitly the admin migration.
```

```text
Bad: On 6.7.3+, keep duplicating every language file as messages.en-GB.json and messages.de-DE.json without base files.
Good: Move shared translations into messages.en.base.json or messages.de.base.json and keep country-specific files only as overrides where needed.
```

```text
Bad: Reuse a 6.7 payment example in a 6.6 plugin without re-checking the archived payment guide.
Good: Verify the exact 6.6 payment-handler contract first, then isolate any version-sensitive seam in one service or adapter.
```

## Replacement Strategy

Prefer small, explicit version seams over scattered conditionals:

- one adapter for version-sensitive admin build logic
- one payment-orchestration seam for handler contract differences
- one snippet or translation compatibility layer when 6.6 and 6.7.3+ filename rules differ
- one dedicated migration chunk when a copied legacy storefront template must be brought back in line with newer core markup

## Official Anchors

Start here when versioned behavior matters:

- 6.7 payment guide: `https://developer.shopware.com/docs/guides/plugins/plugins/checkout/payment/add-payment-plugin.html`
- 6.6 payment guide: `https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/checkout/payment/add-payment-plugin.html`
- 6.7 template guide: `https://developer.shopware.com/docs/guides/plugins/plugins/storefront/customize-templates.html`
- 6.6 template guide: `https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/customize-templates.html`
- 6.7 migrations guide: `https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/database-migrations.html`
- 6.6 migrations guide: `https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/database-migrations.html`
- Vue 3 upgrade: `https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/vue3.html`
- Pinia upgrade: `https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/pinia.html`
- Vite upgrade: `https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/vite.html`
- Translation extension upgrade: `https://developer.shopware.com/docs/resources/references/upgrades/core/translation/extension-translation.html`
