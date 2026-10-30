# Upstream Review Handoff

## Decision and Baselines

Prepare `shopware-knowledge` 0.10.0 as a skills-only contribution to Shopware AI Coding Tools. Keep `shopware-development` as the invocation name and retain standalone installation. No MCP runtime, hooks, required service, or tool pre-approvals are introduced.

| Surface | Baseline |
| --- | --- |
| Source `dev` | `491dd9128a802205035c6720faeb253f33e3d90a` |
| Integrated contribution inventory | `34145c3f4e00eead8aa47b7c948a6a266d53df44`, including original PR #2/#3/#4 commits; CMS was already merged |
| Host repository | [shopwareLabs/ai-coding-tools](https://github.com/shopwareLabs/ai-coding-tools/tree/a276558d12d0e09696fb9d1a7b4cd1925c44baf6) at `a276558d12d0e09696fb9d1a7b4cd1925c44baf6` |
| Core source | v6.7.15.1 at `fc6b754982a0328200ffd3f8d795664a0a6e8447`; targeted v6.6.10.30 at `0c8ec1021b48f217dce2cac5558c933a9aa21b53` |

The review branch in the source repository carries the preservation ledger, correction rationale, behavioral fixtures, and detailed changelog. These are preparation evidence, not a claim that upstream has merged the plugin.

## Review Links

- [Source preparation PR #5](https://github.com/biotech-shopware/claude-shopware-skill/pull/5), targeting `dev`.
- [Upstream PR #203](https://github.com/shopwareLabs/ai-coding-tools/pull/203), targeting `main` from `biotech-shopware:ai-tooling-refactoring` at `bc8d14150f27b010459dd07d35d32ec86b11f7b0`.
- [Source validation workflow](https://github.com/biotech-shopware/claude-shopware-skill/actions/runs/40978155433), passing for the finalized implementation and packaging commit.

The upstream PR is ready for review and mergeable, with maintainer edits enabled. Its external-contribution workflows require maintainer approval. Formal reviewer assignment is unavailable to this contributor account; the maintainer handoff is posted on the PR. No merge or release tag has been performed.

## Reproduce the Contribution

Use a clean checkout of the exact host baseline. From this source repository, inspect the dry run and apply only after reviewing its file list:

```bash
python3 scripts/prepare_upstream.py --host /path/to/ai-coding-tools
python3 scripts/prepare_upstream.py --host /path/to/ai-coding-tools --apply
```

The checked-in [registration patch](../../upstream/registration.patch) changes only the host registries, README, issue registrations, existing Codex registry tests, and Python-bytecode ignore patterns. The script copies the one canonical runtime corpus and namespaces test support; it does not keep a second edited knowledge copy or manipulate remote branches. Host-specific human/maintenance docs are kept in [small wrappers](../../upstream/plugin-docs/README.md).

Expected contribution:

- Canonical plugin under `plugins/shopware-knowledge/`, dual manifests, portable marker, stable topic/applicability/source index, and task-specific examples/templates.
- Both marketplace entries and the root README plugin entry, including Codex support alongside existing dev tooling.
- Generated skill/other-component issue-template entries; no unrelated dropdown additions.
- Focused tests under `plugin-tests/shopware-knowledge/`, support under `scripts/shopware-knowledge/`, and fixtures under `eval/shopware-knowledge/`.
- A namespaced deterministic validation workflow, with required pinned validator dependencies.
- Updated dev-tooling registry assertions that select by name and validate all available entries rather than assuming one plugin or array position zero.

Host wrappers reference host installation commands and maintenance paths; they do not depend on source-only Git history or ledger scripts. Existing `test-writing`, `contributor-writing`, `shopware-env`, and `shopware-documentation` retain specialized workflow ownership. The standalone skill remains usable without them.

## Executed Host Gates

| Check | Result |
| --- | --- |
| Host version validator | All 11 plugin versions synchronized |
| Issue-template generator and validator | Two intended registrations changed; dropdowns current |
| Claude marketplace and plugin validator | Pass |
| Focused package unit tests | 34 pass, including bundled-license rejection and export preservation |
| Required exporter / `skills-ref` / ZIP parity | Pass |
| Topic index and core locator check | 29 records; 89 pinned paths resolve |
| Fixture schema and corrected c10 Composer decode | Pass; host/source fixture bytes match |
| ShellCheck of edited BATS file | Pass |
| Host-pinned BATS framework and focused Codex registry suite | All 28 tests pass |
| Complete host BATS suite | 1,559 pass, no failures/skips; Ubuntu 26.04 ARM64, Git 2.53.0, non-root, eight file workers preserving within-file order |
| Host plugin README/AGENTS/changelog citation lint | All citations resolve; no findings in those wrappers |
| Broader runtime citation/style lint | All 154 checked relative citations resolve; 96 inherited bare-path style findings remain, including three already present in the host README |

Fresh-checkout preparation, strict patch-payload application and final file checks pass; reapplication makes zero changes. The runtime corpus remains byte-identical. Upstream manifest repository/homepage fields adapt to the host while preserving author credit. The registration patch's meaningful context blanks are exempted narrowly from the source repository's whitespace lint; strict `git apply --whitespace=error` still validates its actual payload.

Preparation/apply and whitespace checks must be rerun after content changes. The reproducible script is the handoff path; ephemeral local checkout names and generated patch files are not part of the public contract.

## Review and Publication Gates

1. Review the [preservation ledger](preservation-ledger.md), [correction evidence](corrections.md), [plugin changelog](../../plugins/shopware-knowledge/CHANGELOG.md), and [executed validation](validation-results.md).
2. Review inherited bare-path formatting deliberately. Some entries are instruction operands rather than links; do not turn them into nonexistent links just to silence style checks.
3. Run authenticated Claude behavioral comparisons before asserting dual-runtime decision equivalence. Claude installation/manifest checks pass, but live Claude evaluation is explicitly unverified.
4. Exercise interactive client discovery and project/provider/browser integration where applicable. CLI fixtures are not full application or production verification.
5. Complete review of the open upstream contribution using its [description and QA guide](upstream-pull-request.md). Keep the source preparation branch available for preservation/correction review. Publish version tags/releases only after maintainer approval.

Future MCP retrieval is a [separate deterministic design](retrieval-design.md) over the same corpus. It must preserve examples, source anchors, compatibility boundaries and standalone installation; it is not required for this first contribution.
