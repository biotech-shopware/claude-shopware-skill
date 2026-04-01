---
name: shopware-development
description: >-
  Plan, implement, refactor, or review Shopware 6 changes with Shopware 6.7
  as the default target and explicit Shopware 6.6 compatibility handling.
  Use for plugin development, cart and checkout pipeline work, theme and
  template work, storefront Twig/JS/SCSS changes, accessibility or storefront
  compliance reviews, headless or composable frontend integrations,
  administration modules, app extensions, payment integrations, subscriptions
  and recurring-commerce flows, saved-payment-method ownership issues, testing
  patterns, search and indexing work, i18n and snippet handling, CMS elements,
  import/export work, media handling, Rule Builder conditions, CLI and tooling
  tasks, multichannel context issues, project implementation planning,
  migrations, performance/security hardening, and Shopware code reviews or
  multi-plugin architecture analysis.
allowed-tools: Read, Glob, Grep
---

# Shopware Development

## Overview

Use this skill as base context and guardrails for Shopware work. It must never constrain Claude from using full model capacity for end-to-end review, deep investigation, or broader solution search when the codebase or request requires it.

## Source Discipline

Use sources in this order:
1. Shopware official docs for the exact target version.
2. Stable Shopware core behavior matching `composer.lock`.
3. Symfony official docs.
4. The clustered guidance in this skill.

Treat attached source material, ADRs, issues, forums, and blog posts as context only unless they match the official docs or stable core behavior.

## Workflow

1. Detect the target Shopware version from root `composer.json`, plugin/theme `composer.json`, and `composer.lock`.
2. Use the Read tool on `${CLAUDE_SKILL_DIR}/references/<filename>` to access reference files. Use this routing table before broadening the scan:

| Task signal | Always read | Also read if |
| --- | --- | --- |
| `payment`, `PSP`, `webhook`, `refund`, `vault` | `07` | `15` for recurring, `16` for separate frontend, `18` for cart/checkout payment coupling |
| `cart`, `checkout`, `line item`, `delivery`, `promotion` | `18` | `04` for backend architecture, `07` for payment, `13` for pricing scope |
| `Twig`, `storefront`, `theme`, `SCSS`, `storefront JS` | `05` | `17` for accessibility, `16` for separate frontend |
| `cache`, `http cache`, `varnish`, `reverse proxy` | `04`, `05`, `11` | `10` for exact docs and core anchors |
| `admin`, `app`, `cloud`, `manifest`, `Pinia`, `Vite` | `06` | `02` for migration or version split, `21` for snippets |
| `queue`, `messenger`, `rabbitmq`, `worker`, `async` | `04`, `11`, `14` | `18` for checkout handoff, `20` for indexer-related workers |
| `review`, `audit`, `analysis` | `08` | add the domain refs that match the touched flow |
| `test`, `PHPUnit`, `fixture`, `Store API test` | `19` | `18` for cart, `07` for payments, `20` for indexing |
| `search`, `OpenSearch`, `Elasticsearch`, `listing` | `20` | `04` for DAL, `13` for commerce scope |
| `indexer`, `reindex`, `dal:refresh:index` | `20` | `11` for operational pressure, `14` for worker and command execution |
| `snippet`, `translation`, `locale`, `i18n` | `21` | `05` for storefront text, `06` for admin snippets, `02` for 6.7.3+ base snippets |

3. Read only the relevant reference files for that task. Treat them as starting context, not a hard boundary. Keep following code, evidence, configs, adjacent repos, and official docs when the task requires it.
4. If the task mentions accessibility, ADA, WCAG, VPAT, screen readers, keyboard support, forms, focus, modals, storefront UX, or theme/frontend audits, always read:
   - `${CLAUDE_SKILL_DIR}/references/05-storefront-and-themes.md`
   - `${CLAUDE_SKILL_DIR}/references/10-official-docs-map.md`
   - `${CLAUDE_SKILL_DIR}/references/17-accessibility-and-template-best-practices.md`
5. Inventory mutation surfaces, trust boundaries, ownership boundaries, browser-authored data, cross-plugin contracts, and accessibility-sensitive UI patterns before proposing fixes.
6. Plan the smallest coherent safe change set. One concern per chunk: versioning, data model, cart pipeline, API, UI, payment flow, recurring flow, search/indexing, accessibility remediation, or review findings. If one small shared seam removes obvious duplication or avoids a second near-identical function, widen that seam instead of forcing an artificial micro-change.
7. Preserve extension points and existing project patterns unless the task explicitly includes a migration.
8. For multi-repo reviews, do not finalize findings until a triangulation pass checks how identifiers, saved methods, browser-stored values, custom fields, webhook state, recurring references, snippet or translation contracts, and shared frontend accessibility contracts move across repos.
9. Validate after each chunk with the narrowest useful checks.
10. Report version assumptions, what changed, what was verified, and any remaining regression risk.

## Execution Rules

- Default to Shopware 6.7 guidance. Read 6.6 compatibility notes only when the project or request requires them.
- Keep changes small and reversible, but prefer the smallest coherent safe change over the mechanically smallest diff.
- Apply DRY and KISS by default. Reuse an existing seam or helper when the behavior is genuinely shared instead of cloning near-identical code just to keep the diff smaller.
- Protect hot paths first: cart, checkout, login, account, renewal, and large admin lists.
- Customer-facing mutations must be login-protected, ownership-checked, and `POST`-only unless they are truly read-only.
- Admin write routes must enforce backend `_acl`, not only frontend UI permissions.
- Prefer official extension points over overrides: events, decoration, DAL extensions, Store API/Admin API routes, Twig blocks.
- Keep controllers, subscribers, and handlers thin. Move behavior into services.
- Prefer semantic HTML over ARIA patching. Use ARIA only when the native element cannot express the behavior.
- Use buttons for actions and links for navigation. Do not use `href="#"` pseudo-controls.
- Reusable storefront components must keep IDs unique and `aria-controls`, `aria-labelledby`, and `aria-describedby` relationships valid.
- Custom storefront JS widgets must handle focus entry, focus return, and live status updates where the interaction changes visible state asynchronously.
- Do not treat filename-derived alt text, browser `alert()`, or body-wide DOM repair scripts as acceptable default accessibility fixes.
- Do not use heavy Twig helpers such as `searchMedia()` inside loops or CMS slots when the data can be prepared once upstream.
- Scope storefront plugin selectors to `this.el` or the component root. Avoid broad `document.querySelector(...)` patterns that break repeated components.
- Never trust client-reported payment state, amount, or provider references. Verify amount, currency, state, and recurring references server-side.
- Ownership-check saved methods, provider card-choice records, and subscription payment-method changes by customer and sales-channel context.
- Make webhook, finalize, and callback flows signature-verified or provider-verified and idempotent.
- Review `convertedOrder`, cart snapshots, `customFields`, and `ApiAware` fields as data-exposure surfaces.
- Keep scheduled tasks, reminders, and renewal scans batched, bounded, and keyed off technical names or immutable state, not translated labels.
- Log correlation IDs and redacted metadata, not provider payloads, tokens, signatures, or customer PII.
- Treat `sw-cache-hash` variation, invalidation states, cookies, and cacheable controller markup as reverse-proxy boundaries. Do not break Varnish or CDN cacheability casually.
- Prefer CLI workers with explicit transports and failure queues on production. Treat the admin worker as a development fallback unless the project proves otherwise.
- Indexers must stay bounded: batch with `IteratorFactory`, emit `EntityIndexingMessage`, and keep reindex implications explicit.
- Add safeguards only for concrete failure modes in the actual code path. Do not add redundant casts, null guards, normalization, or wrapper branches when the type contract, DAL contract, validated input, or config contract already guarantees the value.
- Ask before choosing between multiple valid approaches when the choice materially changes save behavior, persistence flow, entity modeling, native-component reuse, or admin/storefront UX structure.
- If data conceptually belongs to the parent entity edit flow, prefer the normal entity save pipeline by default. Do not default to on-click writes inside a tab, editor, or assignment UI unless there is a clear operational reason.
- Keep template logic cheap, admin UIs thin, and background work asynchronous when possible.
- Use the inline examples in the owning reference files as starting patterns, not as a ceiling on implementation design. Adapt them to the exact plugin, Shopware version, and project conventions.

## Reference Map

Read only the files needed for the current task using `${CLAUDE_SKILL_DIR}/references/<filename>`:

- `references/01-source-hierarchy.md`
  source order, file ownership, repo-local `CLAUDE.md` rule.
- `references/02-version-targeting.md`
  6.7/6.6 splits and migration-sensitive behavior.
- `references/03-implementation-workflow.md`
  chunking, validation, regression control, PR structure.
- `references/04-plugin-backend.md`
  backend architecture, DAL, Store API/Admin API, HTTP cache safety, migrations, queues.
- `references/05-storefront-and-themes.md`
  Twig, storefront JS, SCSS, themes, page loaders, SEO, cache-safe rendering, accessibility basics.
- `references/17-accessibility-and-template-best-practices.md`
  WCAG-oriented storefront accessibility reviews and remediation patterns.
- `references/16-headless-and-composable-frontends.md`
  headless or composable frontend trust boundaries and cross-repo contracts.
- `references/06-administration-and-apps.md`
  admin modules, services, ACL, apps, Vue 3, Pinia, Vite.
- `references/07-payments.md`
  payment handlers, redirects, tokenization, webhooks, saved methods, refunds.
- `references/08-analysis-and-reviews.md`
  findings-first review mode, severity, triangulation, review output.
- `references/09-symfony-and-php.md`
  Symfony and PHP rules that matter inside Shopware.
- `references/10-official-docs-map.md`
  official docs and core-source anchors.
- `references/11-quality-and-operations.md`
  security baseline, cache and queue operations, observability, testing, store readiness.
- `references/12-extension-patterns.md`
  config, Flow Builder, CMS, import/export, media, mail, catalog, Rule Builder.
- `references/13-context-and-commerce.md`
  `Context` vs `SalesChannelContext`, pricing, tax, multichannel rules.
- `references/14-cli-and-dev-tooling.md`
  console commands, workers, static analysis, local tooling.
- `references/15-subscriptions-and-recurring-payments.md`
  subscription lifecycle, renewal correctness, saved-method ownership.
- `references/18-cart-and-checkout-pipeline.md`
  collectors, processors, validators, line items, delivery, promotion, recalculation.
- `references/19-testing-patterns.md`
  integration tests, Store API tests, fixtures, repository mocks, migration tests.
- `references/20-search-and-indexing.md`
  search routes, indexers, Elasticsearch/OpenSearch, mapping, reindexing, fallbacks.
- `references/21-internationalization-and-snippets.md`
  storefront/admin snippets, translation associations, fallback inheritance.

## Output Expectations

- State the target Shopware version explicitly when it affects the answer.
- For implementation work, explain the next smallest safe step rather than proposing a broad rewrite.
- When the user asks for a full review or end-to-end analysis, use this skill as context only and keep the investigation open until the relevant surfaces are exhausted.
- For review work, present findings first, ordered by severity and blast radius.
- Pin review findings to the current commit or working tree state. If the codebase changed between runs, say the baseline changed instead of presenting the delta as pure inconsistency.
- When accessibility is a primary scope, put accessibility findings first, map them to WCAG, name the impacted flow, and distinguish confirmed code defects from runtime verification gaps or vendor limitations.
- Every material finding should include the failure mode, blast radius, smallest safe fix, regression note, and validation note.
- Classify non-primary review output clearly when needed: actionable now, deferred by scope, inactive or dormant surface, or verification gap.
- When moving from review to implementation, prefer one finding at a time with a narrow regression pass after each fix. Re-scan the changed surface first unless the user asked for a fresh full review.
- For implementation-ready accessibility reviews, include code samples when the user asks for them.
- When the flow spans multiple plugins or repos, add a separate cross-flow section for contract drift instead of hiding it inside one plugin review.
- When backend and frontend repos share one payment flow, make it explicit which values are browser-authored hints and where server authority is re-established.
- When the user asks for a PR description, merge request description, or release-ready implementation summary, default to the detailed structure from `references/03-implementation-workflow.md` unless the user requested another format.
- For uncertain versioned behavior, say that verification against the exact docs/core tag is required.
