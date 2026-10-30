# feat(shopware-knowledge): add Shopware development knowledge

Shopware development guidance currently lives in separate skill installations. `shopware-knowledge` brings the shared `shopware-development` skill into this marketplace for Claude Code and Codex, with portable export for clients that use standalone skills. The first contribution is skills-only. It needs no MCP server, hooks, credentials, or additional plugin to work.

## Runtime contract

The plugin keeps the `shopware-development` invocation name and targets Shopware 6.7 with explicit 6.6 compatibility. Classic storefront and backend development remain central. Existing Store API and separate-frontend ownership/security boundaries are retained when relevant, without expanding composable-frontend coverage.

The entrypoint selects review, implementation, planning, debugging, or research mode and links directly to the relevant references. Detailed findings and PR/QA templates load only for their task. References do not limit investigation depth or solution breadth. User instructions, repository overlays, and runtime permissions still apply; the knowledge skill grants no permission to edit, run commands, or delegate work.

Installed `test-writing`, `contributor-writing`, `shopware-env`, and `shopware-documentation` retain ownership of their specialized workflows. Standalone Shopware testing context and output templates remain available without those plugins. The corpus is bundled inside the skill, so a portable export does not depend on files outside its installation.

## Knowledge preserved and corrected

The preparation branch accounts for every baseline rule/example as retained, moved, corrected, or retired. It includes the original commits from the local-development, missing-facts, and Administration/storefront contributions; CMS guidance was already present. The upstream commit credits that contribution without importing the source repository's history or maintenance ledger into the marketplace.

| Area | Retained contract or correction |
| --- | --- |
| Backend and DAL | Context/customer/channel scope, bounded criteria, batching, complete reads, migration immutability, ACL, state machines, and lifecycle deployment. Bounded ID reads are distinguished from paginated discovery instead of adding limits that silently truncate work. |
| Cart and checkout | Collector/processor separation, deterministic recalculation, price/tax/delivery/promotion authority, bounded work, and post-order side-effect boundaries. Provider freshness, key inputs, invalidation and final verification replace fixed universal cache durations. |
| Payments and renewals | Server-authoritative amount/currency/state, transaction and saved-method ownership, signed callbacks, operation uniqueness, retries, unknown-outcome reconciliation, refunds, and recurring authority. Optional payment hooks and the after-order validation boundary are explicit. |
| Cache and reverse proxies | Patch/feature-flag-specific response policy, variation, delayed invalidation, hash validation, and rollout checks. Login-state variation is not treated as customer identity. Personalized fragments follow the actual route and cache policy. |
| Queue and search | Durable claims, provider idempotency, redacted correlation logs, retries/failure handling, worker topology, complete indexer lifecycle, targeted reindexing, and search consistency. Delay recommendations remain transport-sensitive. |
| Storefront and accessibility | Block-safe overrides, scoped JS lifecycle, semantic markup, labels, keyboard/focus, repeated IDs, live status, consent and revocation. The cookie helper example uses its verified static contract. |
| Administration, CMS and i18n | Parent save flow, association ownership, compatible component extension, translated slot configuration, resolver loading, snippets, and language inheritance. Local environment instructions require the detected configuration. |
| Review behavior | Evidence-backed severity, baseline pinning, sibling comparison, prior-finding verification and actionable/deferred/inactive triage. No mandatory static-only review, three complete scans, or automatic P1 classification for absent tests. |

Unsupported universal operational thresholds, compulsory diagnostic-tool installation, blanket database prohibitions and unrelated fixed tool-version prescriptions were removed or scoped to evidence. No financial, ownership, cache-isolation or merchant-data-retention invariant was removed to shorten the entrypoint.

The [preservation ledger](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/docs/maintenance/preservation-ledger.md) accounts for 2,457 units: 2,004 retained, 28 moved, 417 corrected, and 8 retired self-check/provenance or unsupported-assertion units. This is accounting, not proof that every sentence is correct. [Correction evidence](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/docs/maintenance/corrections.md) identifies the checked contracts.

## Marketplace integration

| Surface | Behavior |
| --- | --- |
| Claude Code | Minimal marketplace registration plus per-plugin metadata and relative reference links. No editing or state-changing command pre-approvals. |
| Codex | Native `.codex-plugin/plugin.json` with the same skill corpus and `AVAILABLE` marketplace registration. No `agents/openai.yaml` compatibility assumption. |
| Portable Agent Skills | `.agent-skills` opt-in uses the existing exporter and required `skills-ref` validation; the exported body/reference bytes remain unchanged and the original MIT notice travels with every installation. |
| Discoverability | Root README plugin entry, plugin README/AGENTS/changelog, and generated skill/component issue registrations follow the existing layout. |
| Registry tests | The existing dev-tooling Codex assertions select plugins by name and validate every registered entry instead of assuming a single entry at array index zero. Existing dev-tooling runtime files are untouched. |
| Maintainer support | Topic/applicability/source metadata, isolated package tests and fixed evaluation fixtures live under plugin-namespaced paths. Generated Python bytecode is ignored. A read-only CI job makes no model calls. |

`knowledge-index.json` holds stable topic identifiers, version/feature applicability and source anchors. The agent does not classify the corpus on every request. Filtered MCP delivery can use the same index later, but no retrieval server or embedding dependency is introduced here.

## Validation performed

Checks were rerun against upstream `a276558d12d0e09696fb9d1a7b4cd1925c44baf6`. Core investigation used Shopware `v6.7.15.1` with targeted `v6.6.10.30` comparisons.

| Gate | Observed result |
| --- | --- |
| Package contracts | 34 focused tests pass, including invalid metadata, escaping/broken references, duplicate IDs, missing/blank bundled-license rejection, export preservation and isolated runner behavior. |
| Native and portable packaging | Claude marketplace/plugin validation, native metadata, host exporter, required `skills-ref`, YAML/frontmatter and ZIP byte-parity checks pass. |
| Source locators | All 89 pinned core paths resolve in the actual tag objects; this checks path existence, not the semantics of every surrounding rule. |
| Index and fixtures | 29 deterministic topic records and all 14 fixed fixture schemas/Composer targets pass. Rubrics are kept outside model workspaces. |
| Host integration | All plugin versions synchronized, issue-template registrations current, all 28 focused Codex registry BATS tests pass, and ShellCheck passes. |
| Installation | Actual source-branch GitHub installation through the official Codex skill installer and Claude marketplace installer succeeds; installed runtime bytes match the candidate. Codex native marketplace catalog discovery also succeeds. |
| Codex behavior | Independent semantic review of 14 paired fixed cases preserves expected defects and keeps clean/compatibility controls clean, with no new unsupported P0/P1 observed. Selected financial/ownership/cache cases were repeated; natural-language discovery and a downloaded-skill smoke test also pass. |
| Privacy and formatting | No personal paths, private conversation URLs or runtime-specific invocation prose in the skill. Relative links resolve and diff whitespace checks pass. Synthetic privacy-test strings are deliberate controls. |

The paired cases cover payment authority, ownership, renewal retries, cart I/O, cache isolation, concurrent queue work, indexers, translated CMS configuration, parent save flow, lifecycle deployment, accessibility, 6.6 compatibility and valid controls. They are small review fixtures, not full Shopware applications. Arm order was not randomized and these observations do not establish statistical superiority or universal finding stability.

## QA guide

Use a clean checkout of this PR. Run the following from the repository root in one Python environment with the pinned dependencies installed:

```bash
python3 -m pip install -r eval/shopware-knowledge/requirements.txt
python3 -m unittest discover -s plugin-tests/shopware-knowledge -p 'test_*.py' -v
python3 scripts/shopware-knowledge/build_knowledge_index.py --check
python3 scripts/shopware-knowledge/validate_skill_pack.py
python3 eval/shopware-knowledge/run.py check
.github/scripts/validate-versions.sh
.github/scripts/validate-issue-templates.sh
.bats/bats-core/bin/bats plugin-tests/dev-tooling/codex_manifest.bats
claude plugin validate .
git diff --check
```

The package validator invokes the existing portable exporter and `skills-ref`; missing validation dependencies fail rather than turning into a skipped success. The fixture `check` command does not invoke a model. Set up the repository's pinned BATS dependencies first with `.github/scripts/setup-bats.sh` if necessary.

1. Add this checkout as a separate local marketplace in a disposable Claude configuration. Install `shopware-knowledge` and verify it is enabled at `0.10.0`; invoke `/shopware-knowledge:shopware-development`. Expect the relevant relative references to resolve with no MCP setup or external permission granted by the skill.
2. Register this checkout in a disposable Codex configuration or install its standalone skill through the existing installer. Verify discovery of `shopware-development`, then ask a payment, cache or CMS question. Expect the matching topic references, not the entire corpus, to be read.
3. Review the pricing/ownership/queue fixture examples and valid controls in `eval/shopware-knowledge/cases.json`. Inspect both the proposed failure flow and the clean-control expectation before running a model.
4. For an explicitly authorized live check, run `python3 eval/shopware-knowledge/run.py run --case c13 --runtime codex --skill plugins/shopware-knowledge/skills/shopware-development --execute`. Expect the valid formatter to remain clean and fixture hashes to stay unchanged. Without `--execute`, the runner only prints its plan.
5. In authenticated Claude Code, repeat with `--runtime claude`, then run the relevant paired cases before claiming dual-runtime behavioral equivalence. Authentication is required; package installation alone is not that proof.
6. Check coexistence with `test-writing`, `contributor-writing`, `shopware-env` and `shopware-documentation`. Expect the specialized installed workflow to own its task, with the domain reference available as context and a standalone fallback when the other plugin is absent.
7. Check duplicate skill discovery. An older manual `shopware-development` installation should not be mistaken for the new plugin; remove only the intended redundant copy. Do not overwrite active global skills as part of QA.

## Risk and remaining verification

The runtime change is instruction behavior, not application code. Regressions could include missed topic routing, misleading version assumptions, speculative review findings or conflicts with specialized plugins. The preservation ledger, negative fixtures, source anchors, portable-byte checks and namespaced tests address those risks without asserting that every possible project is covered.

Claude live model tests remain unverified because the available CLI is not authenticated. Native packaging and actual Claude installation pass. Interactive IDE/app discovery, real Shopware/container integration, browser/assistive-technology behavior, provider enforcement, concurrency recovery and reverse-proxy/search rollout still require their own environments. PHP snippets were linted on PHP 8.5, not a separate PHP 8.2 runtime.

All runtime citations resolve. The host's broader style checker still reports inherited bare-path style findings in the corpus; some are literal instruction operands. These are not unresolved links, and the PR does not claim a clean strict-style run. The plugin's human-facing wrappers pass the citation/style check.

The full host BATS suite was attempted locally, then stopped when unrelated ChunkHound cases failed because `ugrep` is not installed on the Mac. The changed 28-test Codex registry suite passes. Upstream Linux CI installs that prerequisite and must provide the full-suite result; the interrupted local run is not counted as a pass.

## Scope and release

`0.10.0` is prepared metadata, not a published release. No tags, existing release histories, active global installs, unrelated plugin runtimes or user configuration are changed. The optional MCP retrieval layer remains a separate follow-up. Monthly source/framework/PHPStan review is documented as a maintenance cadence, not an installed background job.

## References

- [Source preparation branch](https://github.com/biotech-shopware/claude-shopware-skill/tree/ai-tooling-refactoring)
- [Detailed plugin changelog](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/plugins/shopware-knowledge/CHANGELOG.md)
- [Executed validation and limitations](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/docs/maintenance/validation-results.md)
- [Reproducible upstream preparation](https://github.com/biotech-shopware/claude-shopware-skill/blob/ai-tooling-refactoring/docs/maintenance/upstream-handoff.md)
