# Optional Filtered Knowledge Delivery

Status: design only; not required for installation and not shipped as an MCP runtime.

## Contract

The canonical corpus remains `plugins/shopware-knowledge/skills/shopware-development/`. A later adapter reads `knowledge-index.json` at build time and exposes deterministic topic lookup by stable ID, Shopware version, mode, feature flag, and text terms. It needs no embeddings, remote service, credentials, or model classification.

Return the owning rule with its example, applicability, source anchors, and adjacent safety boundaries; never return an isolated sentence whose omitted context changes its meaning. Unknown versions/flags produce explicit applicability uncertainty, not silent exclusion.

## Acceptance Gates

- Portable skill works offline with every required reference bundled.
- Retrieval selects the same applicable invariants as the portable form on fixed payment, cart, cache, queue, indexing, CMS, lifecycle, accessibility, and 6.6 cases.
- Stable identifiers survive wording changes. Splits have aliases/redirects; removed rules have recorded dispositions.
- Retrieval output is bounded and paginated but never silently truncates a requested topic or its examples.
- Packaging, rule ownership, and source maintenance are shared; no second independently edited knowledge copy.
- Measure tokens, coverage, false positives, latency, and installation cost before making retrieval a default.
