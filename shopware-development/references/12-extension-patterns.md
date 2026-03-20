# Extension Patterns

## Plugin Configuration

- Use `config.xml` and a typed configuration wrapper for merchant-facing settings.
- Read configuration with sales-channel awareness when the behavior can vary by channel.
- Validate and normalize config values before use; do not pipe raw config values directly into clients.
- Keep shop-specific secrets in Shopware configuration, not hardcoded constants or generic environment variables meant for one global value.
- API URL, timeout, debug mode, and feature flags belong in plugin configuration with a typed service, not in `private const` values scattered across services.
- When writing custom fields programmatically, merge with the existing custom field array instead of replacing unrelated keys.

## Business Events and Flow Builder

- Dispatch explicit business events for meaningful domain actions instead of hardcoding follow-up emails, tags, or webhooks.
- Use Flow Builder-compatible events when merchants should be able to react without code changes.
- Implement custom flow actions when the plugin exposes a domain operation merchants should be able to call from Flow Builder.
- Put the business decision in the service, then emit the event once state is committed.
- When a subscription or approval state changes, dispatch one event and let Flow Builder or other subscribers handle mail, tagging, and webhook actions.

## CMS Elements and Blocks

- Split CMS work into admin registration, storefront template, data resolver, and data struct responsibilities.
- Load data in the resolver and attach a struct to the slot; do not query inside Twig.
- Keep configuration-driven ordering and defaults explicit.
- A custom product slider should collect product IDs in `collect()`, enrich the slot in `enrich()`, and render a prepared struct in Twig.

## Import and Export

- Prefer Shopware import/export profiles, field mappings, and serializers over raw CSV loops.
- Chunk large imports and track progress or logs for resumability.
- Keep mapping rules explicit for nested fields, translations, media, and custom fields.
- Add custom serializers or converters when external data formats need normalization instead of baking conversion logic into controllers or commands.
- A product sync profile should map `price.DEFAULT.gross`, tax, media, and custom fields instead of manually parsing rows into repository writes.

## Media Handling

- Use Shopware media services, file savers, folders, and associations rather than writing directly into public media paths.
- Validate remote sources before downloading them and treat URL-based imports as SSRF-sensitive.
- Keep folder configuration and thumbnail behavior explicit.
- Upload a remote image through `MediaService` or `FileSaver`, create the media entity first, then associate the media ID to products or CMS content.

## Rule Builder Conditions

- Use custom rules when pricing, shipping, promotions, or content need merchant-configurable conditions.
- Match the correct scope and expose configuration via `RuleConfig`.
- Keep payload lookups and custom-field reads deterministic.
- A customer-tier rule or product custom-field rule should use typed operators and scopes instead of scattering conditional checks across checkout services.

## Custom Line Item Types

- Use a dedicated line item type for plugin-specific discounts, credits, fees, or bundle markers.
- Do not identify your business logic by translated labels or by reusing a generic line item type such as `credit`.
- Store credit should be a dedicated `store_credit` line item with explicit payload or extensions, not a generic credit item guessed by label text like "Store credit discount".

## Mail and Notification Patterns

- Keep transactional email ownership explicit. Do not hardcode mail sends across random subscribers when Flow Builder, business events, or one orchestration service should own the decision.
- Customize mail templates and payloads through stable extension points, not copy-pasted mail-rendering logic in controllers.
- Do not block hot paths on email delivery when the business flow can durably queue or defer the send.

Example pattern:

```text
Bad: send mail directly from every state-transition subscriber that notices the same order change.
Good: dispatch one business event after the state is committed and let Flow Builder or one mail orchestration path send the notification.
```

## Product and Catalog Extension Choices

- Use custom fields for light editorial product metadata.
- Use entity extensions when the product needs structured extra fields but the lifecycle still belongs to the product.
- Use custom entities when the domain needs its own lifecycle, synchronization, batching, or indexes.
- Keep variant, property, stream, and cross-selling logic aligned with existing Shopware catalog models before inventing plugin-side shortcuts.

Example pattern:

```text
Bad: store variant-generation rules and stream membership as unindexed product customFields and query them at scale.
Good: use Shopware property groups, product streams, or a dedicated custom entity when the data drives operational catalog behavior.
```
