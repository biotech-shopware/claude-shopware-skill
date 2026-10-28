# Changelog

## [0.10.0] - Unreleased

### Packaging and Integration

- Package `shopware-knowledge` in the Shopware AI Coding Tools plugin layout, retaining the `shopware-development` skill trigger and all domain owners. Add Claude/Codex manifests, marketplace registration, portable export, and source/applicability metadata without a required MCP service.
- Integrate the local-development, missing-facts, and Administration/storefront contributions with their original commits. Preserve CMS guidance already present on `dev`.
- Remove tool pre-approvals and runtime-specific UI metadata. Let installed host plugins own their specialized workflows, with standalone fallbacks.
- Add a dry-run-first upstream preparation adapter and narrow registration patch. Preserve one runtime corpus while adapting host metadata, documentation, namespaced validation and registry tests reproducibly.

### Instruction Quality

- Replace duplicate entrypoint descriptions and global execution rules with mode selection and direct relative topic links. Preserve one explicit constraint against limiting reasoning, investigation, or solution breadth.
- Keep detailed PR/QA and findings templates in task-specific references. Make review depth, runtime validation, report creation, and patch output follow the request and risk rather than a mandatory static-only three-pass format.
- Preserve enumeration, sibling comparison, source-of-record checks, prior-finding verification, DRY/KISS, coherent changes, and high-impact direction-choice discipline. Assign severity from evidence and impact, not missing-test counts or category labels.

### Technical Corrections

- Correct static cookie-helper use and consent lifecycle behavior; preserve scoped storefront initialization, repeated-component safety, semantic markup, and keyboard/focus requirements.
- Replace fixed cart-cache TTL/key/invalidation requirements with provider-specific freshness and authority contracts; keep deterministic recalculation and request deduplication.
- Clarify feature-flag-dependent HTTP cache variation, hash validation, response policy, and reverse-proxy rollout checks. Remove unsupported catalog-size thresholds and mandatory diagnostic-tool installation.
- Distinguish bounded ID reads from paginated discovery; preserve batch completeness. Clarify normal versus explicitly invoked destructive migrations and deployment/version triggers.
- Treat payment and renewal timeouts as unknown outcomes requiring reconciliation. Preserve server authority, ownership, signed callbacks, operation uniqueness, and financial-state consistency.
- Retain complete indexer contracts, targeted versus full reindex routes, transport-sensitive delay restrictions, complete test fixtures, CMS translations, and 6.6 compatibility boundaries.

### Verification and Maintenance

- Add a unit-level preservation ledger, fixed behavioral fixtures with clean controls, package/manifest checks, source anchors, and isolated installation/export checks. Executed results and remaining gaps are reported separately; fixture existence is not a claim of runtime validation.
- Document monthly source/framework/PHPStan review and a separate deterministic MCP retrieval design over the same corpus. No MCP runtime ships in this iteration.

Earlier release history remains in the [repository changelog](../../CHANGELOG.md).
