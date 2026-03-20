# Analysis and Reviews

Use review mode when the user asks for:

- a code review
- an accessibility or storefront compliance audit
- a security or performance audit
- architecture analysis
- regression risk assessment
- upgrade-safety review

- Pin the Shopware version from project files before judging best practices.
- Use official Shopware docs, matching core behavior, and Symfony docs as the basis for recommendations.
- When linking core behavior, pin links to the exact Shopware tag or commit from `composer.lock` when possible.
- Treat ADRs, issues, forum posts, and blog posts as labeled context unless verified.
- Treat this skill as review context, not a scan boundary. For full reviews, keep following evidence across the full relevant surface even when the initially loaded references are narrow.

## Scope Coverage

Scan the full affected scope rather than just the first suspicious file:

- backend services, subscribers, controllers, routes, DAL definitions, migrations, commands, handlers, and DI config
- storefront Twig, JS, SCSS, theme overrides, and SEO-sensitive surfaces
- separate frontend repos, composables, SDK loaders, browser storage, client interceptors, and payment UI contracts when they participate in the same flow
- administration modules, permissions, build compatibility, and app surfaces
- config, queue, logging, environment-sensitive code, and CI hooks
- translations and snippet filename conventions when localization is touched

## Scan Order

Prioritize the highest-risk surfaces first:

If accessibility is the primary review goal, inspect navigation, forms, focus management, modal or offcanvas flows, repeated-card components, and async status messaging before lower-risk storefront detail.

1. security boundaries
2. ownership or IDOR exposure and state-changing `GET` routes
3. payment correctness, webhook authenticity, and finalize authority
4. cart, checkout, login, account, and recurring renewal hot paths
5. admin ACL and operational safety
6. cache, invalidation, indexer, queue, and scheduled-task behavior
7. DAL query shape, migrations, data exposure, and large-instance impact
8. storefront performance and SEO
9. accessibility when the request or surface makes it material
10. extensibility and upgrade safety

## Severity Model

- P0
  Security vulnerabilities, payment trust-boundary failures, hot-path regressions, cache-collapse risks, broken idempotency.
- P1
  Large performance problems outside the hottest flows, migration/index risks, broad admin or storefront regressions.
- P2
  Maintainability, lower-risk upgrade issues, or testing gaps that still matter.

If the repo is clean, say so directly and mention residual testing or verification gaps instead of inventing findings.

## Big-Instance Stress Model

Assume production scale unless the repo proves otherwise:

- large catalogs and customer tables
- many sales channels and languages
- heavy imports and queue usage
- Redis, reverse proxy, CDN, and background workers

For each important finding, explain:

- what breaks first at scale
- the complexity shape or unbounded behavior
- the cache, queue, or DB blast radius

Also check whether the issue only appears when multiple plugins share one customer flow. If so, call that out as cross-plugin contract drift instead of pretending it is isolated to one repo.
If backend and frontend repos share one payment flow, trace exactly which values are browser-authored, which are server-resolved, and where provider truth is re-established.

## Evidence Rules

Every material finding should include:

- exact file path and symbol, with line references when practical
- impacted flow or surface
- WCAG mapping when accessibility is in scope
- a realistic failure mode or regression scenario
- the trust boundary that is broken or missing
- the blast radius in production
- the smallest fix direction that matches Shopware patterns
- copyable inline references as raw URLs in backticks when a source is cited

For review output that includes diffs, add:

- a regression note
- a validation note
- a compatibility-impact note if the safest fix changes a public contract

## Review Output

Default format:

- findings first
- ordered by severity and impact
- each finding names the file or surface, the risk, and the smallest safe fix direction

When accessibility is a primary scope:

- group accessibility findings first
- map each accessibility finding to WCAG criteria
- distinguish confirmed code defects from runtime verification gaps
- distinguish local code issues from vendor or third-party widget limitations
- include code examples when the user asks for implementation-ready review output

For multi-repo or plugin-ecosystem reviews, structure the output as:

- per-repo findings
- one cross-flow section for shared contracts, recurring references, saved-method ownership, or payment-method-change ordering
- a short validation or tooling-limits section

Avoid checklist spam. Only report material issues that are actually present.

Literal findings template:

```md
### [P0/P1/P2] Title

- **File:** `/absolute/path/to/file.php:123`
- **Flow:** `checkout -> payment -> webhook`
- **Failure mode:** [what breaks or what can be abused]
- **Blast radius:** [which users or systems are affected and at what scale]
- **Smallest safe fix:** [what to change without forcing a rewrite]
- **Regression risk:** [what adjacent surface could still break]
- **Validation:** [how to verify the fix]
```

Accessibility-first variant:

```md
### [P0/P1/P2] Accessibility Title

- **Surface:** `checkout confirm`
- **WCAG:** `4.1.2 Name, Role, Value`
- **Failure mode:** [keyboard, screen-reader, focus, label, or status issue]
- **Blast radius:** [which journey is blocked or degraded]
- **Smallest safe fix:** [semantic HTML, focus handling, status region, etc.]
- **Validation:** [keyboard path, browser/AT verification, and code-level check]
```

## Writing Style

- Write like a senior engineer, not a pasted system checklist.
- Keep sentences short and decisive.
- Avoid filler and speculative noise.
- If there are no findings, say so clearly and mention remaining verification gaps instead of padding the report.

## Triangulation Reviews

Use a triangulation pass when multiple repos or plugins share one business flow, especially subscriptions plus PSP integrations.

Before finalizing findings:

- map shared identifiers, custom fields, saved-method records, and provider references across repos
- map browser-stored values, frontend request payloads, and backend authority boundaries across repos
- verify which repo is authoritative for each state transition and payment decision
- check whether one repo assumes validation or ownership enforcement that another repo never performs
- split local code issues from cross-plugin contract drift so the implementation order stays clear
