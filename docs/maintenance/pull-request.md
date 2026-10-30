# Prepare shopware-knowledge 0.10.0 for Shopware AI Coding Tools

## Description

### Problem

The development skill contains valuable Shopware knowledge, but its packaging and several instructions are not yet suitable for a skills-only contribution to Shopware AI Coding Tools. The entrypoint repeats domain policy, review mode imposes static-only three-pass execution and severity-dependent patch formats, and some examples encode unsupported universal cache, queue, migration, and operational assumptions.

The preparation also needs to preserve the pending contributor work rather than replace the existing corpus with a shorter but weaker summary.

### Why This Matters

Incorrect knowledge can generate incorrect plugin code or false high-priority review findings. Packaging compatibility cannot be inferred from a YAML parse or from one runtime ignoring unsupported metadata. The proposed contribution must remain simple to install, version-aware, and equally usable without an MCP service.

This is **0.10.0 preparation**, not a published release or an upstream merge. The live Claude behavioral gate remains explicitly open.

### Implementation

- Integrate the original commits from #2, #3, and #4 on this branch, preserving authorship. CMS work from #1 was already present in the pinned dev baseline.
- Package the plugin as `plugins/shopware-knowledge/` with Claude and Codex manifests, both marketplace entries, and a self-contained `skills/shopware-development/` corpus. Keep the invocation name unchanged and remove editing/shell pre-approvals and `agents/openai.yaml`.
- Replace numeric routing and repeated global rules with mode selection and direct relative references. The entrypoint is approximately 64% smaller by word count, while one explicit constraint preserves unlimited investigation and solution breadth.
- Preserve all 28 numbered owners, the detailed PR/QA and findings templates, business invariants, and concrete examples. Separate the Messenger implementation into a bounded reference.
- Correct consent lifecycle/static-helper use, actual cache variation and feature-flag behavior, provider-derived quote freshness, bounded DAL discovery, destructive migration sequencing, durable side-effect idempotency, and unknown payment/renewal outcomes.
- Replace category-based automatic P0/P1 assignments and missing-test severity with evidence/impact-based review. Keep enumeration, sibling comparisons, prior-finding verification, source-of-record checks, and explicit verification gaps.
- Add stable topic/applicability/source metadata, a unit-level preservation ledger, primary-source correction evidence, fixed behavioral fixtures and clean controls, required export validation, and reproducible upstream preparation.
- Let installed test-writing, contributor-writing, documentation, and environment plugins retain their specialized workflows. Keep standalone guidance available when they are absent.
- Prepare host registration, issue-template, README, and Codex registry-test changes through a narrow patch plus dry-run-first adapter. Adapt host metadata/docs without maintaining a second runtime corpus. MCP retrieval remains a separate deterministic design only.

### Affected Plugin Areas

- Discovery, routing, source/version research, implementation and review behavior.
- Backend/DAL, lifecycle/deployment, cart/checkout, payments, renewals, cache/Varnish, Messenger, and indexing.
- Classic storefront, consent/accessibility, Administration parent-save behavior, translated CMS data, snippets, and local-environment safety.
- Claude/Codex native manifests, portable export, installation instructions, upstream registries, validation, and maintenance.

### Risk and Regression Assessment

The main compatibility change is the installable path and plugin name; `shopware-development` remains the skill name. Existing standalone installations can duplicate the plugin and should be deliberately removed/disabled when switching. This branch does not replace active global skills automatically.

Every one of 2,457 baseline units has a disposition: 2,004 retained, 28 moved, 417 corrected, and eight redundant self-check/provenance or unsupported-assertion units retired. That is preservation accounting, not proof of every technical statement. Matching-source evidence and behavioral checks are separate.

On the executed small Codex cases, expected findings were preserved, clean controls stayed clean, and no new unsupported P0/P1 was observed. The experiment is not randomized and does not establish statistical superiority or universal stability. Full Shopware/provider/browser integration, interactive IDE/app discovery, and authenticated Claude behavior are not claimed.

### Validation Performed

- 34 focused package tests pass, including missing/blank bundled-license rejection and license-preserving export parity.
- Required pinned host exporter, skills-ref validation, normalized portable frontmatter, reference bytes, and ZIP parity pass.
- All 29 topic records are indexed; 89 pinned core source paths resolve in actual Shopware v6.7.15.1/v6.6.10.30 Git objects.
- Claude plugin/marketplace validators pass; both local-marketplace and GitHub-branch one-command installations succeed in isolated configurations, with installed runtime files matching the source.
- Official Codex GitHub skill installer succeeds into a temporary destination; downloaded runtime files match the source. Native Codex marketplace catalog recognizes version 0.10.0.
- 14 paired Codex cases receive independent semantic review, plus repeated payment/ownership/renewal/cache cases and two unprefixed discovery probes. Rubrics remain outside model-visible fixtures.
- Two defective initial fixtures were corrected and rerun in both arms; their superseded outputs are excluded. One capacity failure is not scored as a semantic failure and is retried with the same model.
- On the pinned host checkout, all 11 plugin versions and generated issue registrations validate; all 28 focused Codex registry BATS tests pass. Fresh preparation works and reapplication makes zero changes.
- Current-tree privacy and relative-file-link checks pass. Host citation paths resolve; inherited bare-path style warnings remain documented rather than silently exempted or converted into fictitious links.

### QA Notes

1. Start from a clean checkout of the pinned host revision. Run `python3 scripts/prepare_upstream.py --host /path/to/ai-coding-tools`, review the planned files, then repeat with `--apply`. Confirm a second application proposes zero changes and no index/branch/remote mutation.
2. Run host version/issue checks, the 34 package tests, portable exporter/skills-ref checks, fixture schema checks, and the 28 Codex registry BATS tests. Missing validation dependencies must fail, not skip.
3. Test standalone and marketplace discovery with no duplicate older installation. Use explicit invocation and a natural-language Shopware request separately. Verify actual domain-reference reads, not only a catalog entry.
4. Re-run the fixed payment, ownership, renewal, cart, cache, queue, indexing, CMS, save-flow, lifecycle, accessibility, and 6.6 cases. Check both valid and rejection paths and retain the clean controls.
5. Run the same behavioral comparison in authenticated Claude Code before claiming dual-runtime equivalence. Installation succeeds without that model gate; a missing login is not a behavioral pass.
6. Verify real target-version container/browser/provider/proxy behavior where it is relevant. Static evidence does not prove production enforcement, accessibility conformance, search consistency, or crash recovery.
7. Review the inherited bare-path style warnings and the source correction/preservation records. Publish tags/releases only after maintainer review; do not merge directly into upstream as part of this preparation.

## Review Material

- [Detailed changelog](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/plugins/shopware-knowledge/CHANGELOG.md)
- [Preservation ledger](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/docs/maintenance/preservation-ledger.md)
- [Correction evidence](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/docs/maintenance/corrections.md)
- [Executed validation and remaining gates](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/docs/maintenance/validation-results.md)
- [Reproducible upstream handoff](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/docs/maintenance/upstream-handoff.md)
