# Administration and Apps

Index: admin rules, admin Twig, 6.7/6.6 surfaces, apps, cloud, manifest, webhooks, actions, scripts, validation.

Decide first whether the task belongs in:

- a plugin administration module
- a Shopware app extension
- a project-local admin customization

Use the lightest surface that fits the requirement.

## Administration Rules

- Keep admin UI thin. Heavy work belongs in backend services and Admin API routes.
- Prefer System Config for simple settings pages. Build a full admin module only when the workflow justifies it.
- Enforce ACL in both UI and backend.
- Use repository access, Criteria, and service utilities consistently.
- Use the documented administration extension surfaces rather than ad hoc global bridges between modules.
- Never embed secrets, private keys, or privileged provider credentials in admin JS.
- If the feature integrates an external API, prefer a clear diagnostics path such as an API test action and actionable error reporting.
- Never expose Admin API tokens, client secrets, or equivalent privileged credentials to storefront JavaScript or Twig.
- Do not make the storefront call custom Admin API routes directly. Bridge through a backend route with the correct customer-facing validation or use the Store API where appropriate.
- Ask before choosing between multiple valid admin directions when the decision materially changes save behavior, write timing, entity modeling, native-component reuse, or UX structure.
- If plugin-owned data belongs to an entity edit surface, prefer saving through the normal entity save flow by default instead of issuing immediate writes from a tab or embedded editor.

Example patterns:

```js
// Bad: storefront bridge to privileged admin route
fetch('/api/_action/my-plugin/rebuild-index', {
    method: 'POST',
    headers: { Authorization: `Bearer ${adminToken}` },
});
```

```text
Preferred: keep the privileged action in the admin or app backend, protect it with ACL or signed app requests, and expose only customer-safe storefront routes through Store API or another ownership-checked backend route.
```

## Administration Twig Templates

- Administration Twig templates do not have access to storefront-only PHP Twig functions.
- Administration templates are automatically extended; do not add `{% extends '...' %}` or `{% sw_extends '...' %}`.
- A block with the same name replaces the parent block. Use `{% parent %}` only when appending to parent content is intentional.

```text
Bad: a new category tab writes cross-selling rows immediately on every click even though the data belongs to the category edit flow.
Good: extend the category save flow by default and only choose immediate writes when the user explicitly wants that UX or the scale justifies it.
```

## 6.7 Migration Surfaces

Treat these as explicit modernization tasks:

- Vue 3 migration
- Pinia store migration
- Vite build migration

Use them only when the project already targets them or the user asked for the migration.

## 6.6 Compatibility Mode

For 6.6 work:

- verify the admin surface against `/docs/v6.6/` when available
- keep transition-era code stable unless the migration is the task
- avoid mixing admin modernization with unrelated feature work
- if the plugin must support both 6.6 and 6.7 admin builds, assume a version split or build split may be necessary and verify it explicitly

## App Extensions

Use app surfaces when the requirement fits the app model:

- manifest-driven configuration
- custom modules
- action buttons
- webhooks
- app scripts
- custom fields and extension surfaces declared through the manifest

## Cloud and App-First Guidance

- If the target is Shopware Cloud, assume app-first constraints unless the project proves it is self-hosted.
- Prefer apps when the requirement fits manifest-declared permissions, Admin API or Store API access, webhooks, action buttons, custom modules, or app scripts.
- Prefer plugins only when the project is self-hosted and the feature truly needs plugin-only capabilities such as PHP runtime extensions, DAL entity definitions, migrations, or storefront plugin code.
- Do not design cloud features around filesystem writes, direct DB access, or plugin-only extension points that cannot exist in the app model.

Concrete scope examples:

```text
Bad: pick a plugin admin module for a cloud-compatible settings form that only needs config, action buttons, and one backend webhook.
Good: use an app with manifest permissions, a custom module, and a signed backend for the webhook or action flow.
```

```text
Bad: force an app script to own a workflow that actually needs durable operational state, batch processing, and server-side retries.
Good: if the project is self-hosted and the flow needs DAL entities, queues, and PHP services, keep it in a plugin.
```

## App Manifest Rules

- Keep `manifest.xml` complete and least-privilege. Do not request permissions "just in case".
- Declare only the hosts, cookies, webhooks, payment methods, tax providers, and custom fields the app actually needs.
- Keep compatibility explicit and align manifest features with the supported Shopware versions.
- If the app only needs to read orders and trigger one action button, do not request create/update/delete permissions across unrelated entities.

## App Webhooks

- Verify signatures before processing.
- Make handlers idempotent and safe for retries.
- Return success only after the event is durably accepted; return failure when you need Shopware to retry.
- Queue or defer slow downstream sync logic.
- `product.written` should upsert sync state keyed by the Shopware entity ID instead of blindly creating duplicate remote records.

## Action Buttons and Admin Actions

- Verify signed action payloads on the app backend.
- Handle single-item and bulk actions deliberately.
- Return the right action response type for UX: notification, modal, new tab, or reload.
- Keep privileged writes on the app backend or Admin API; never trust client-side action payloads by themselves.
- A "Sync to ERP" action should return a success or error notification, while a "Show report" action can open a modal or new tab.

## App Scripts

- Use app scripts for light hook-based behavior that does not need a full admin module or plugin backend.
- Do not hide complex business logic in Twig scripts when the flow deserves a service or app backend endpoint.
- Prefer app scripts or manifest-declared extension points when they solve the task cleanly; do not escalate to a full plugin or admin module without a reason.

## Validation

For admin or app changes, verify:

- ACL and route permissions
- translation and snippet resolution
- build path used by the project
- error states and progress handling
- no leakage of secrets into client bundles
- no mixed Vuex and Pinia assumptions during 6.7 migration work
- dependency hygiene when adding SDKs or large NPM packages to the admin bundle
- least-privilege app permissions, webhook signature handling, and action-button response behavior
- no storefront-to-admin credential bridging or browser-side use of admin tokens

## 6.7 Administration Changes

### Vite + Pinia + Vue 3

- Admin builds with Vite. Webpack is out.
- Vue 2 compat layer is removed.
- Components are async by default. Template refs may not exist pre-`@vue:mounted`; guard with the event or `nextTick`.
- State management uses Pinia via `Shopware.Store.register({ id, state, getters, actions })`.
- Vuex helpers renamed to `mapVuexState`, `mapVuexMutations`, `mapVuexGetters`, `mapVuexActions` (legacy). New code uses Pinia's `mapState`.
- `vue-i18n` v10 drops `tc`. `$tc` is still shimmed to `$t` — migrate to `$t('key', { count })` now.

A separate plugin version is required per major (6.7+).

Source: UPGRADE-6.7.md §6.7.0.0, release notes 6.7.0.

### Meteor Components (`mt-*`)

Many `sw-*` primitives are renamed. Full mapping:

- `sw-button` → `mt-button`
- `sw-text-field` → `mt-text-field`
- `sw-select-field` → `mt-select`
- `sw-card` → `mt-card`
- `sw-tabs` → `mt-tabs`
- `sw-icon` → `mt-icon`
- `sw-checkbox-field` → `mt-checkbox`
- `sw-datepicker` → `mt-datepicker`
- `sw-password-field` → `mt-password-field`
- `sw-colorpicker` → `mt-colorpicker`
- `sw-external-link` → `mt-external-link`
- `sw-progress-bar` → `mt-progress-bar`
- `sw-switch-field` → `mt-switch`
- `sw-number-field` → `mt-number-field`
- `sw-loader` → `mt-loader`
- `sw-textarea-field` → `mt-textarea`
- `sw-email-field` → `mt-email-field`
- `sw-url-field` → `mt-url-field`
- `sw-skeleton-bar` → `mt-skeleton-bar`
- `sw-popover` → `mt-floating-ui`

Prefer `mt-*` in 6.7 templates. Fall back to `sw-*` only when explicitly targeting 6.6. `mt-*` enforces Shopware Design System — expect behavioral changes beyond prop renames.

To run one codebase across 6.6 and 6.7, set `deprecated="true"` on `sw-*` components to preserve old behavior.

Source: UPGRADE-6.7.md §6.7.0.0.

### Admin Codemod

Run codemods for admin migration:

```bash
composer run admin:code-mods -- --plugin-name MyPlugin --fix -v 6.7
```

- Requires the plugin to live under `custom/plugins/`.
- Adds `// TODO` comments where manual work is required. Do not assume 100% automation.

### `sw-entity-listing` `items` → `dataSource`

From 6.7.8, passing `items` to `sw-entity-listing` is deprecated. Pass `:dataSource="…"` instead.

Source: release notes 6.7.8.

### Rule Builder Condition Contract

- `LineItemPurchasePriceRule`: `bool $isNet` → `?string $type` (`'gross'|'net'`, auto-migrated).
- `LineItemCustomFieldRule` now throws `RuleException::unsupportedOperator()` (not `CartException`).
- `CustomerBirthdayRule` no longer throws on null.
- `LineItemProductStatesRule` deprecated → `LineItemProductTypeRule`.
- Rule builder condition components `sw-condition-line-item-in-category`, `-purchase-price`, `-is-net-select` are deprecated for `sw-condition-generic`.
- `sw-condition-base` no longer exposes `mapPropertyErrors('condition', […])` spreads or `conditionValue*Error` computeds. Use `sw-condition-field-errors` and read errors off the entity's error collection.

Source: UPGRADE-6.7.md §6.7.12.0, §6.7.13.0.

### Filesystem `visibility`

`filesystems.<name>.config.visibility` is deprecated. Use `filesystems.<name>.visibility` at the top level in generated `config/packages/shopware.yaml` snippets.

Source: UPGRADE-6.7.md §6.7.1.0.

### OAuth `scope` Format

`/api/oauth/token` requires space-delimited `scope: 'write admin'` (a string, not an array). Array form silently fails. `/api/oauth/authorize` is removed.

Source: UPGRADE-6.7.md §6.7.0.0.

### MCP Server Integration

Experimental MCP endpoints at `/api/_mcp` and `/store-api/_mcp` — active whenever `symfony/mcp-bundle` is installed (the `MCP_SERVER` feature flag is removed in 6.7.14).

Register capabilities with DI tags:

- `mcp.tool`
- `mcp.prompt`
- `mcp.resource`

CLI: `bin/console debug:mcp` lists registered capabilities. Classes are `@experimental` until 6.8 — do not inherit from them.

Source: release notes 6.7.11, UPGRADE-6.7.md §6.7.14.

### Payment/Shipping `technicalName` Non-Nullable

`payment_method.technical_name` and `shipping_method.technical_name` are non-nullable in 6.7 (auto-migrated). Always set a plugin-prefixed `technicalName` in plugin migrations and method creation. Custom field set `name` must be unique per app (from 6.7.1). Payment or shipping methods without `technicalName` at upgrade time get `temporary_<id>` assigned automatically — set meaningful names before upgrade or lose the ability to reference them cleanly.

Source: release notes 6.7.0, 6.7.1.
