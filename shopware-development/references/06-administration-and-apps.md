# Administration and Apps

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
